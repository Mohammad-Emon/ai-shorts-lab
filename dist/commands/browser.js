import { BrowserManager } from "../browser/BrowserManager.js";
const browser = new BrowserManager();
async function ensureStarted() {
    try {
        await browser.start();
    }
    catch { }
}
export async function handleBrowserCommand(req) {
    await ensureStarted();
    try {
        switch (req.type) {
            case "browser.openTab": {
                const { tabId, url } = req.payload ?? {};
                if (!tabId)
                    throw new Error("tabId required");
                await browser.openTab(tabId, { url });
                return ok(req, { tabId, url });
            }
            case "browser.goto": {
                const { tabId, url } = req.payload ?? {};
                const page = getPage(tabId);
                await page.goto(url);
                return ok(req, { tabId, url });
            }
            case "browser.click": {
                const { tabId, selector } = req.payload ?? {};
                const page = getPage(tabId);
                await page.click(selector);
                return ok(req, { clicked: selector });
            }
            case "browser.type": {
                const { tabId, selector, text } = req.payload ?? {};
                const page = getPage(tabId);
                await page.fill(selector, text);
                return ok(req, { filled: selector });
            }
            case "browser.screenshot": {
                const { tabId, path } = req.payload ?? {};
                const page = getPage(tabId);
                await page.screenshot({ path });
                return ok(req, { path });
            }
            default:
                return fail(req, `Unhandled browser command: ${req.type}`);
        }
    }
    catch (err) {
        return fail(req, err?.message ?? String(err));
    }
}
function getPage(tabId) {
    if (!tabId)
        throw new Error("tabId required");
    const page = browser.getTab(tabId);
    if (!page)
        throw new Error(`Tab not found: ${tabId}`);
    return page;
}
function ok(req, result) {
    return { requestId: req.requestId, success: true, result, completedAt: Date.now() };
}
function fail(req, message) {
    return { requestId: req.requestId, success: false, error: { message }, completedAt: Date.now() };
}
