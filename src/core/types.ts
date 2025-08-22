export type AgentId = string;

export type AgentStatus =
	| "idle"
	| "initializing"
	| "running"
	| "waiting"
	| "error"
	| "completed";

export interface AgentState<TContext = Record<string, unknown>> {
	id: AgentId;
	name: string;
	status: AgentStatus;
	context: TContext;
	createdAt: number;
	updatedAt: number;
}

export interface CommandRequest<TPayload = unknown> {
	type: string;
	payload?: TPayload;
	requestId: string;
	issuedAt: number;
}

export interface CommandResult<TResult = unknown> {
	requestId: string;
	success: boolean;
	result?: TResult;
	error?: { message: string; code?: string };
	completedAt: number;
}

export type AgentEventType =
	| "state:changed"
	| "command:received"
	| "command:completed"
	| "log";

export interface AgentEvent<T = unknown> {
	type: AgentEventType;
	payload: T;
	timestamp: number;
}