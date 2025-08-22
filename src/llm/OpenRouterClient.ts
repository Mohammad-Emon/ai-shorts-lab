import fetch from "node-fetch";

export type StreamChunk = { content: string; isFinal?: boolean };

export interface OpenRouterConfig {
	apiKey?: string;
	baseUrl?: string;
	defaultModel?: string;
}

export class OpenRouterClient {
	private apiKey: string;
	private baseUrl: string;
	private defaultModel: string;

	constructor(config: OpenRouterConfig = {}) {
		this.apiKey = config.apiKey ?? process.env.OPENROUTER_API_KEY ?? "";
		this.baseUrl = config.baseUrl ?? "https://openrouter.ai/api/v1";
		this.defaultModel = config.defaultModel ?? process.env.OPENROUTER_MODEL ?? freeDefaultModel();
		if (!this.apiKey) {
			console.warn("OPENROUTER_API_KEY not set; requests will fail until provided.");
		}
	}

	async completeChat(messages: { role: "system" | "user" | "assistant"; content: string }[], model?: string): Promise<string> {
		const chosenModel = model ?? this.defaultModel;
		const url = `${this.baseUrl}/chat/completions`;
		const res = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${this.apiKey}`,
			},
			body: JSON.stringify({ model: chosenModel, messages }) as any,
		});
		if (!res.ok) {
			const text = await res.text();
			throw new Error(`OpenRouter error ${res.status}: ${text}`);
		}
		const json = (await res.json()) as any;
		return json?.choices?.[0]?.message?.content ?? "";
	}

	async streamChat(
		messages: { role: "system" | "user" | "assistant"; content: string }[],
		onChunk: (chunk: StreamChunk) => void,
		model?: string
	): Promise<void> {
		const chosenModel = model ?? this.defaultModel;
		const url = `${this.baseUrl}/chat/completions`;
		const res = await fetch(url, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${this.apiKey}`,
			},
			body: JSON.stringify({ model: chosenModel, messages, stream: true }) as any,
		});
		if (!res.ok || !res.body) {
			const text = await res.text().catch(() => "");
			throw new Error(`OpenRouter stream error ${res.status}: ${text}`);
		}
		const reader = (res.body as any).getReader();
		const decoder = new TextDecoder();
		let buffer = "";
		while (true) {
			const { value, done } = await reader.read();
			if (done) break;
			buffer += decoder.decode(value, { stream: true });
			let idx: number;
			while ((idx = buffer.indexOf("\n\n")) !== -1) {
				const packet = buffer.slice(0, idx).trim();
				buffer = buffer.slice(idx + 2);
				for (const line of packet.split("\n")) {
					const trimmed = line.trim();
					if (!trimmed) continue;
					if (trimmed === "data: [DONE]") {
						onChunk({ content: "", isFinal: true });
						return;
					}
					if (!trimmed.startsWith("data:")) continue;
					const payload = trimmed.slice(5).trim();
					try {
						const json = JSON.parse(payload);
						const delta = json?.choices?.[0]?.delta?.content ?? "";
						if (delta) onChunk({ content: delta });
					} catch {}
				}
			}
		}
		onChunk({ content: "", isFinal: true });
	}
}

function freeDefaultModel(): string {
	// Favor a commonly available free/auto model on OpenRouter.
	return process.env.OPENROUTER_FREE_MODEL ?? "openrouter/auto";
}