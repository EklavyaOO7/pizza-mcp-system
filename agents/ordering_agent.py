import json
import re
import requests
from mcp_server.api_server import execute_tool
from a2a.protocol import send

OLLAMA_URL = "http://localhost:11434/api/generate"


class OrderingAgent:

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def parse_order(self, text):
        prompt = (
            "Extract pizza name and size from the text.\n"
            "Return ONLY valid JSON. No markdown. No explanation.\n\n"
            f"Text: {text}\n\n"
            "JSON format:\n"
            '{"pizza": "<name>", "size": "<size>"}'
        )

        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        data = resp.json()

        # ✅ Handle BOTH Ollama response formats
        if "response" in data:
            raw = data["response"]
        elif "message" in data and "content" in data["message"]:
            raw = data["message"]["content"]
        else:
            raise RuntimeError(f"Unexpected Ollama response:\n{data}")

        # 🔧 Remove markdown if present
        raw = re.sub(r"```json|```", "", raw).strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON from Ollama:\n{raw}")

    def handle(self, text):
        print(f"\n👤 User: {text}")

        order = self.parse_order(text)

        result = execute_tool(
            "post__order",
            order
        )

        print("🍕 Order confirmed:", result)

        send("OrderingAgent", self.scheduler, result)
