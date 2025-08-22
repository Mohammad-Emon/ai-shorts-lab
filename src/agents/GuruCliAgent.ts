import { v4 as uuidv4 } from "uuid";
import { AgentEventBus } from "../core/eventBus.js";
import { AgentStateStore } from "../core/state.js";
import type { AgentState, AgentStatus, CommandRequest, CommandResult } from "../core/types.js";

export type CommandHandler = (request: CommandRequest) => Promise<CommandResult> | CommandResult;

export interface AgentConfig<TContext extends Record<string, unknown> = Record<string, unknown>> {
	name: string;
	initialContext?: TContext;
}

export class GuruCliAgent<TContext extends Record<string, unknown> = Record<string, unknown>> {
	readonly id: string;
	readonly name: string;
	protected bus: AgentEventBus;
	protected state: AgentStateStore<TContext>;
	protected handlers: Map<string, CommandHandler> = new Map();

	constructor(config: AgentConfig<TContext>) {
		this.id = uuidv4();
		this.name = config.name;
		this.bus = new AgentEventBus();
		const initial: AgentState<TContext> = {
			id: this.id,
			name: this.name,
			status: "idle",
			context: (config.initialContext ?? {}) as TContext,
			createdAt: Date.now(),
			updatedAt: Date.now(),
		};
		this.state = new AgentStateStore<TContext>(initial, this.bus);
	}

	onEvent<TPayload = unknown>(type: "state:changed" | "command:received" | "command:completed" | "log", listener: (event: { type: string; payload: TPayload; timestamp: number }) => void) {
		return this.bus.on(type as any, listener as any);
	}

	setStatus(status: AgentStatus) {
		this.state.update((prev) => ({ ...prev, status }));
	}

	registerCommand(type: string, handler: CommandHandler) {
		this.handlers.set(type, handler);
	}

	async handle(request: CommandRequest): Promise<CommandResult> {
		this.bus.emit("command:received", request);
		const handler = this.handlers.get(request.type);
		if (!handler) {
			const res: CommandResult = {
				requestId: request.requestId,
				success: false,
				error: { message: `Unknown command: ${request.type}`, code: "UNKNOWN_COMMAND" },
				completedAt: Date.now(),
			};
			this.bus.emit("command:completed", res);
			return res;
		}
		try {
			const result = await handler(request);
			const res: CommandResult = {
				requestId: request.requestId,
				success: result.success,
				result: result.result,
				error: result.error,
				completedAt: Date.now(),
			};
			this.bus.emit("command:completed", res);
			return res;
		} catch (err: any) {
			const res: CommandResult = {
				requestId: request.requestId,
				success: false,
				error: { message: err?.message ?? String(err) },
				completedAt: Date.now(),
			};
			this.bus.emit("command:completed", res);
			return res;
		}
	}
}