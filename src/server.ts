import http from "http";
import path from "path";
import fs from "fs";
import url from "url";
import { OpenRouterClient } from "./llm/OpenRouterClient.js";

const client = new OpenRouterClient();
const PORT = Number(process.env.PORT || 8787);
const publicDir = path.join(process.cwd(), "public");

function serveFile(req: http.IncomingMessage, res: http.ServerResponse) {
	let pathname = url.parse(req.url || "/").pathname || "/";
	if (pathname === "/") pathname = "/index.html";
	const filePath = path.join(publicDir, pathname);
	if (!filePath.startsWith(publicDir)) {
		res.writeHead(403); res.end("Forbidden"); return;
	}
	fs.readFile(filePath, (err, data) => {
		if (err) { res.writeHead(404); res.end("Not Found"); return; }
		const ext = path.extname(filePath);
		const type = ext === ".html" ? "text/html" : ext === ".js" ? "text/javascript" : ext === ".css" ? "text/css" : "application/octet-stream";
		res.writeHead(200, { "Content-Type": type });
		res.end(data);
	});
}

function sseHeaders() {
	return {
		"Content-Type": "text/event-stream",
		"Cache-Control": "no-cache, no-transform",
		Connection: "keep-alive",
		"Access-Control-Allow-Origin": "*",
	};
}

function mockStream(prompt: string, write: (data: string) => void, end: () => void) {
	const text = `Mock response for: ${prompt}`;
	let i = 0;
	const timer = setInterval(() => {
		if (i >= text.length) { clearInterval(timer); write("data: [DONE]\n\n"); end(); return; }
		write(`data: ${JSON.stringify({ choices: [{ delta: { content: text[i++] } }] })}\n\n`);
	}, 20);
}

const server = http.createServer(async (req, res) => {
	const parsed = url.parse(req.url || "/", true);
	if (req.method === "GET" && parsed.pathname === "/api/stream") {
		res.writeHead(200, sseHeaders());
		const prompt = String((parsed.query?.q as string) || "Hello");
		const messages = [{ role: "user" as const, content: prompt }];
		const write = (d: string) => res.write(d);
		const end = () => res.end();
		if (process.env.OPENROUTER_API_KEY) {
			try {
				await client.streamChat(messages, (chunk) => {
					if (chunk.isFinal) { write("data: [DONE]\n\n"); end(); }
					else write(`data: ${JSON.stringify({ choices: [{ delta: { content: chunk.content } }] })}\n\n`);
				});
			} catch (e: any) {
				write(`data: ${JSON.stringify({ error: e?.message || String(e) })}\n\n`);
				write("data: [DONE]\n\n");
				end();
			}
		} else {
			mockStream(prompt, write, end);
		}
		return;
	}
	serveFile(req, res);
});

if (process.env.NODE_ENV !== "test") {
	server.listen(PORT, () => {
		console.log(`Demo server listening on http://localhost:${PORT}`);
	});
}

export default server;