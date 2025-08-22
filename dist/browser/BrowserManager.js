import { chromium } from "playwright";
export class BrowserManager {
    browser;
    context;
    pages = new Map();
    async start() {
        if (this.browser)
            return;
        this.browser = await chromium.launch({ headless: true });
        this.context = await this.browser.newContext();
    }
    async stop() {
        await this.context?.close();
        await this.browser?.close();
        this.pages.clear();
        this.browser = undefined;
        this.context = undefined;
    }
    async openTab(id, options = {}) {
        if (!this.context)
            throw new Error("Browser not started");
        const page = await this.context.newPage();
        this.pages.set(id, page);
        if (options.url)
            await page.goto(options.url);
        return page;
    }
    getTab(id) {
        return this.pages.get(id);
    }
    async closeTab(id) {
        const page = this.pages.get(id);
        if (page)
            await page.close();
        this.pages.delete(id);
    }
}
