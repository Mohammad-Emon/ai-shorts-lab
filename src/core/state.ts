import { deepStrictEqual } from "assert";
import { AgentEventBus } from "./eventBus.js";
import type { AgentState } from "./types.js";

export class AgentStateStore<TContext extends Record<string, unknown> = Record<string, unknown>> {
	private current: AgentState<TContext>;
	private bus: AgentEventBus;

	constructor(initial: AgentState<TContext>, bus: AgentEventBus) {
		this.current = initial;
		this.bus = bus;
	}

	get(): AgentState<TContext> {
		return this.current;
	}

	update(mutator: (prev: AgentState<TContext>) => AgentState<TContext>): AgentState<TContext> {
		const next = mutator(this.current);
		if (!shallowEqual(this.current, next)) {
			this.current = { ...next, updatedAt: Date.now() };
			this.bus.emit("state:changed", this.current);
		}
		return this.current;
	}
}

function shallowEqual(a: unknown, b: unknown) {
	try {
		deepStrictEqual(a, b);
		return true;
	} catch {
		return false;
	}
}