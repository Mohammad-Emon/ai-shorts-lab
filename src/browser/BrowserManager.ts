import { chromium, Browser, BrowserContext, Page } from "playwright";

export interface OpenTabOptions {
	url?: string;
}

export class BrowserManager {
	private browser?: Browser;
	private context?: BrowserContext;
	private pages: Map<string, Page> = new Map();

	async start(): Promise<void> {
		if (this.browser) return;
		this.browser = await chromium.launch({ headless: true });
		this.context = await this.browser.newContext();
	}

	async stop(): Promise<void> {
		await this.context?.close();
		await this.browser?.close();
		this.pages.clear();
		this.browser = undefined;
		this.context = undefined;
	}

	async openTab(id: string, options: OpenTabOptions = {}): Promise<Page> {
		if (!this.context) throw new Error("Browser not started");
		const page = await this.context.newPage();
		this.pages.set(id, page);
		if (options.url) await page.goto(options.url);
		return page;
	}

	getTab(id: string): Page | undefined {
		return this.pages.get(id);
	}

	async closeTab(id: string): Promise<void> {
		const page = this.pages.get(id);
		if (page) await page.close();
		this.pages.delete(id);
	}
}