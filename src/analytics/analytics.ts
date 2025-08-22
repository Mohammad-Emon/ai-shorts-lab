import { createLogger, format, transports } from "winston";

export const analytics = createLogger({
	level: process.env.LOG_LEVEL || "info",
	format: format.combine(
		format.timestamp(),
		format.json()
	),
	transports: [new transports.Console()],
});

export function track(event: string, data?: Record<string, unknown>) {
	analytics.info("analytics", { event, ...data });
}