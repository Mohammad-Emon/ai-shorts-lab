export class WorkflowManager {
    queue = [];
    timer;
    schedule(id, task, delayMs = 0) {
        this.queue.push({ id, runAt: Date.now() + delayMs, task });
        this.queue.sort((a, b) => a.runAt - b.runAt);
        this.tick();
    }
    tick() {
        if (this.timer)
            return;
        const next = this.queue[0];
        if (!next)
            return;
        const wait = Math.max(0, next.runAt - Date.now());
        this.timer = setTimeout(async () => {
            this.timer = undefined;
            const job = this.queue.shift();
            if (!job)
                return;
            try {
                await job.task();
            }
            finally {
                this.tick();
            }
        }, wait);
    }
}
