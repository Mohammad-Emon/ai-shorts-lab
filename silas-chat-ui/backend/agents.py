"""
Multi-Agent System for Silas Chat UI
Different AI agents with specialized roles that collaborate
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import asyncio
from openai import OpenAI
import os

class AgentRole(Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    ANALYST = "analyst"
    SUMMARIZER = "summarizer"

@dataclass
class AgentMessage:
    agent_id: str
    role: AgentRole
    content: str
    confidence: float
    metadata: Dict[str, Any]
    timestamp: str

@dataclass
class WorkflowTask:
    task_id: str
    user_query: str
    required_agents: List[AgentRole]
    current_step: int
    results: Dict[str, Any]
    status: str  # "pending", "in_progress", "completed", "failed"

class AIAgent:
    def __init__(self, role: AgentRole, model: str, client: OpenAI):
        self.role = role
        self.model = model
        self.client = client
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self) -> str:
        prompts = {
            AgentRole.COORDINATOR: """You are the Coordinator Agent. Your role is to:
- Analyze user queries and determine which agents are needed
- Route tasks to appropriate specialist agents
- Synthesize responses from multiple agents
- Ensure coherent final responses
Keep responses concise and well-structured.""",

            AgentRole.RESEARCHER: """You are the Research Agent. Your role is to:
- Gather factual information and data
- Provide accurate, well-sourced answers
- Focus on facts, statistics, and verified information
- Be thorough but concise in your research findings.""",

            AgentRole.CREATIVE: """You are the Creative Agent. Your role is to:
- Generate creative ideas and solutions
- Write engaging content and stories
- Brainstorm innovative approaches
- Think outside the box while being practical.""",

            AgentRole.TECHNICAL: """You are the Technical Agent. Your role is to:
- Solve programming and technical problems
- Explain complex technical concepts
- Provide code examples and solutions
- Focus on accuracy and best practices.""",

            AgentRole.ANALYST: """You are the Analyst Agent. Your role is to:
- Analyze data and identify patterns
- Provide insights and recommendations
- Break down complex problems
- Offer strategic thinking and planning.""",

            AgentRole.SUMMARIZER: """You are the Summarizer Agent. Your role is to:
- Synthesize information from other agents
- Create clear, concise summaries
- Ensure key points are highlighted
- Make complex information accessible."""
        }
        return prompts.get(self.role, "You are a helpful AI assistant.")
    
    async def process(self, query: str, context: Dict[str, Any] = None) -> AgentMessage:
        """Process a query and return agent response"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": query}
            ]
            
            # Add context if provided
            if context:
                context_str = f"Context from other agents: {json.dumps(context, indent=2)}"
                messages.insert(-1, {"role": "user", "content": context_str})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            return AgentMessage(
                agent_id=f"{self.role.value}_agent",
                role=self.role,
                content=content,
                confidence=0.8,  # Could be calculated based on response
                metadata={"model": self.model, "tokens": len(content.split())},
                timestamp=str(asyncio.get_event_loop().time())
            )
            
        except Exception as e:
            return AgentMessage(
                agent_id=f"{self.role.value}_agent",
                role=self.role,
                content=f"Error processing request: {str(e)}",
                confidence=0.0,
                metadata={"error": str(e)},
                timestamp=str(asyncio.get_event_loop().time())
            )

class MultiAgentOrchestrator:
    def __init__(self, client: OpenAI, free_models: List[str]):
        self.client = client
        self.free_models = free_models
        self.agents = self._initialize_agents()
        self.active_workflows: Dict[str, WorkflowTask] = {}
        
    def _initialize_agents(self) -> Dict[AgentRole, AIAgent]:
        """Initialize all agents with different models for diversity"""
        agents = {}
        
        # Distribute models across agents for variety
        model_assignments = {
            AgentRole.COORDINATOR: self.free_models[0] if self.free_models else "gpt-3.5-turbo",
            AgentRole.RESEARCHER: self.free_models[1] if len(self.free_models) > 1 else self.free_models[0],
            AgentRole.CREATIVE: self.free_models[2] if len(self.free_models) > 2 else self.free_models[0],
            AgentRole.TECHNICAL: self.free_models[3] if len(self.free_models) > 3 else self.free_models[0],
            AgentRole.ANALYST: self.free_models[4] if len(self.free_models) > 4 else self.free_models[0],
            AgentRole.SUMMARIZER: self.free_models[0] if self.free_models else "gpt-3.5-turbo",
        }
        
        for role, model in model_assignments.items():
            agents[role] = AIAgent(role, model, self.client)
            
        return agents
    
    async def process_query(self, user_query: str, session_id: str) -> Dict[str, Any]:
        """Main entry point for multi-agent processing"""
        
        # Step 1: Coordinator determines workflow
        coordinator_response = await self.agents[AgentRole.COORDINATOR].process(
            f"Analyze this user query and determine which specialist agents should handle it: '{user_query}'"
        )
        
        # Step 2: Determine required agents based on query type
        required_agents = self._determine_required_agents(user_query)
        
        # Step 3: Execute multi-agent workflow
        if len(required_agents) > 1:
            return await self._execute_collaborative_workflow(user_query, required_agents, session_id)
        else:
            # Single agent response
            agent_role = required_agents[0] if required_agents else AgentRole.COORDINATOR
            response = await self.agents[agent_role].process(user_query)
            return {
                "response": response.content,
                "workflow_type": "single_agent",
                "agents_used": [agent_role.value],
                "confidence": response.confidence,
                "metadata": response.metadata
            }
    
    def _determine_required_agents(self, query: str) -> List[AgentRole]:
        """Determine which agents are needed based on query analysis"""
        query_lower = query.lower()
        required_agents = []
        
        # Technical queries
        if any(word in query_lower for word in ['code', 'programming', 'technical', 'debug', 'api', 'software']):
            required_agents.append(AgentRole.TECHNICAL)
        
        # Research queries
        if any(word in query_lower for word in ['what is', 'how does', 'explain', 'research', 'facts', 'data']):
            required_agents.append(AgentRole.RESEARCHER)
        
        # Creative queries
        if any(word in query_lower for word in ['create', 'write', 'story', 'idea', 'brainstorm', 'creative']):
            required_agents.append(AgentRole.CREATIVE)
        
        # Analysis queries
        if any(word in query_lower for word in ['analyze', 'compare', 'evaluate', 'recommend', 'strategy']):
            required_agents.append(AgentRole.ANALYST)
        
        # Complex queries that need multiple perspectives
        if len(query.split()) > 15 or '?' in query and len(required_agents) > 1:
            required_agents.append(AgentRole.SUMMARIZER)
        
        # Default to coordinator if no specific agents identified
        if not required_agents:
            required_agents.append(AgentRole.COORDINATOR)
            
        return required_agents
    
    async def _execute_collaborative_workflow(self, query: str, required_agents: List[AgentRole], session_id: str) -> Dict[str, Any]:
        """Execute a collaborative workflow with multiple agents"""
        
        workflow_id = f"{session_id}_{len(self.active_workflows)}"
        workflow = WorkflowTask(
            task_id=workflow_id,
            user_query=query,
            required_agents=required_agents,
            current_step=0,
            results={},
            status="in_progress"
        )
        
        self.active_workflows[workflow_id] = workflow
        
        try:
            # Step 1: Parallel processing by specialist agents
            specialist_tasks = []
            for agent_role in required_agents:
                if agent_role != AgentRole.SUMMARIZER:  # Summarizer runs last
                    task = self.agents[agent_role].process(query)
                    specialist_tasks.append((agent_role, task))
            
            # Wait for all specialist agents to complete
            specialist_results = {}
            for agent_role, task in specialist_tasks:
                result = await task
                specialist_results[agent_role.value] = result
            
            # Step 2: Synthesize results if summarizer is needed
            if AgentRole.SUMMARIZER in required_agents:
                synthesis_context = {
                    "original_query": query,
                    "agent_responses": {k: v.content for k, v in specialist_results.items()}
                }
                
                synthesis_query = f"Synthesize the following agent responses into a coherent answer for: '{query}'"
                final_response = await self.agents[AgentRole.SUMMARIZER].process(
                    synthesis_query, 
                    synthesis_context
                )
                
                workflow.results["final_response"] = final_response
                workflow.status = "completed"
                
                return {
                    "response": final_response.content,
                    "workflow_type": "collaborative",
                    "agents_used": [role.value for role in required_agents],
                    "agent_responses": {k: v.content for k, v.content in specialist_results.items()},
                    "confidence": final_response.confidence,
                    "workflow_id": workflow_id
                }
            else:
                # Combine responses from multiple agents
                combined_response = self._combine_agent_responses(specialist_results, query)
                workflow.status = "completed"
                
                return {
                    "response": combined_response,
                    "workflow_type": "parallel",
                    "agents_used": [role.value for role in required_agents],
                    "agent_responses": {k: v.content for k, v in specialist_results.items()},
                    "workflow_id": workflow_id
                }
                
        except Exception as e:
            workflow.status = "failed"
            return {
                "response": f"Multi-agent workflow encountered an error: {str(e)}",
                "workflow_type": "error",
                "agents_used": [],
                "error": str(e)
            }
    
    def _combine_agent_responses(self, agent_results: Dict[str, AgentMessage], original_query: str) -> str:
        """Combine responses from multiple agents into a coherent answer"""
        
        if len(agent_results) == 1:
            return list(agent_results.values())[0].content
        
        combined = f"Here's what our specialist agents found regarding '{original_query}':\n\n"
        
        for agent_role, message in agent_results.items():
            agent_name = agent_role.replace('_', ' ').title()
            combined += f"**{agent_name}**: {message.content}\n\n"
        
        return combined.strip()
    
    def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowTask]:
        """Get the status of a specific workflow"""
        return self.active_workflows.get(workflow_id)
    
    def list_active_workflows(self) -> List[WorkflowTask]:
        """List all active workflows"""
        return list(self.active_workflows.values())