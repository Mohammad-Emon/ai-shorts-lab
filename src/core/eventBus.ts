import EventEmitter from "eventemitter3";
import type { AgentEvent, AgentEventType } from "./types.js";

export class AgentEventBus {
	private emitter: EventEmitter;

	constructor() {
		this.emitter = new EventEmitter();
	}

	on<TPayload = unknown>(type: AgentEventType, listener: (event: AgentEvent<TPayload>) => void) {
		this.emitter.on(type, listener as any);
		return () => this.emitter.off(type, listener as any);
	}

	emit<TPayload = unknown>(type: AgentEventType, payload: TPayload) {
		const event: AgentEvent<TPayload> = { type, payload, timestamp: Date.now() };
		this.emitter.emit(type, event);
	}
}