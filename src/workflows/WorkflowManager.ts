type TaskFn = () => Promise<void> | void;

export class WorkflowManager {
	private queue: { id: string; runAt: number; task: TaskFn }[] = [];
	private timer?: NodeJS.Timeout;

	schedule(id: string, task: TaskFn, delayMs = 0) {
		this.queue.push({ id, runAt: Date.now() + delayMs, task });
		this.queue.sort((a, b) => a.runAt - b.runAt);
		this.tick();
	}

	private tick() {
		if (this.timer) return;
		const next = this.queue[0];
		if (!next) return;
		const wait = Math.max(0, next.runAt - Date.now());
		this.timer = setTimeout(async () => {
			this.timer = undefined;
			const job = this.queue.shift();
			if (!job) return;
			try { await job.task(); } finally { this.tick(); }
		}, wait);
	}
}