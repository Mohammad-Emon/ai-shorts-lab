import EventEmitter from "eventemitter3";
export class AgentEventBus {
    emitter;
    constructor() {
        this.emitter = new EventEmitter();
    }
    on(type, listener) {
        this.emitter.on(type, listener);
        return () => this.emitter.off(type, listener);
    }
    emit(type, payload) {
        const event = { type, payload, timestamp: Date.now() };
        this.emitter.emit(type, event);
    }
}
