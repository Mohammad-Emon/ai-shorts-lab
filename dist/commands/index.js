export function buildCommandMap(defs) {
    const map = new Map();
    for (const def of defs) {
        map.set(def.type, def.handler);
    }
    return map;
}
