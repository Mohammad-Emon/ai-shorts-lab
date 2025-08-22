import { GuruCliAgent } from "./agents/GuruCliAgent.js";
import { v4 as uuidv4 } from "uuid";
async function main() {
    const agent = new GuruCliAgent({ name: "Guru" });
    agent.onEvent("state:changed", (e) => {
        console.log("state:", e.payload);
    });
    agent.registerCommand("ping", (req) => ({
        requestId: req.requestId,
        success: true,
        result: { pong: true },
        completedAt: Date.now(),
    }));
    const request = {
        type: "ping",
        requestId: uuidv4(),
        issuedAt: Date.now(),
    };
    const result = await agent.handle(request);
    console.log("result:", result);
}
main().catch((err) => {
    console.error(err);
    process.exit(1);
});
