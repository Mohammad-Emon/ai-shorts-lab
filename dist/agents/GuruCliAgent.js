import { v4 as uuidv4 } from "uuid";
import { AgentEventBus } from "../core/eventBus.js";
import { AgentStateStore } from "../core/state.js";
export class GuruCliAgent {
    id;
    name;
    bus;
    state;
    handlers = new Map();
    constructor(config) {
        this.id = uuidv4();
        this.name = config.name;
        this.bus = new AgentEventBus();
        const initial = {
            id: this.id,
            name: this.name,
            status: "idle",
            context: (config.initialContext ?? {}),
            createdAt: Date.now(),
            updatedAt: Date.now(),
        };
        this.state = new AgentStateStore(initial, this.bus);
    }
    onEvent(type, listener) {
        return this.bus.on(type, listener);
    }
    setStatus(status) {
        this.state.update((prev) => ({ ...prev, status }));
    }
    registerCommand(type, handler) {
        this.handlers.set(type, handler);
    }
    async handle(request) {
        this.bus.emit("command:received", request);
        const handler = this.handlers.get(request.type);
        if (!handler) {
            const res = {
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
            const res = {
                requestId: request.requestId,
                success: result.success,
                result: result.result,
                error: result.error,
                completedAt: Date.now(),
            };
            this.bus.emit("command:completed", res);
            return res;
        }
        catch (err) {
            const res = {
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
