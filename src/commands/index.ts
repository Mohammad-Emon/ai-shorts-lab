import type { CommandRequest, CommandResult } from "../core/types.js";

export type CommandDefinition = {
	type: string;
	handler: (req: CommandRequest) => Promise<CommandResult> | CommandResult;
};

export function buildCommandMap(defs: CommandDefinition[]): Map<string, CommandDefinition["handler"]> {
	const map = new Map<string, CommandDefinition["handler"]>();
	for (const def of defs) {
		map.set(def.type, def.handler);
	}
	return map;
}