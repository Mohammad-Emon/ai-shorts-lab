import { deepStrictEqual } from "assert";
export class AgentStateStore {
    current;
    bus;
    constructor(initial, bus) {
        this.current = initial;
        this.bus = bus;
    }
    get() {
        return this.current;
    }
    update(mutator) {
        const next = mutator(this.current);
        if (!shallowEqual(this.current, next)) {
            this.current = { ...next, updatedAt: Date.now() };
            this.bus.emit("state:changed", this.current);
        }
        return this.current;
    }
}
function shallowEqual(a, b) {
    try {
        deepStrictEqual(a, b);
        return true;
    }
    catch {
        return false;
    }
}
