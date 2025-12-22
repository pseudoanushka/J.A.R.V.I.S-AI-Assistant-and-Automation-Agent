import json
import datetime
import http.client
from pathlib import Path
from dotenv import dotenv_values
from google import genai

# ============================================================
# CONFIGURATION
# ============================================================

env = dotenv_values(".env")

USERNAME = env.get("Username")
ASSISTANT_NAME = env.get("AssistantName")
GEMINI_KEY = env.get("GEMINIAPIKey")
SERPER_KEY = env.get("SERPER_API_KEY")

if not GEMINI_KEY or not SERPER_KEY:
    raise RuntimeError("Missing GEMINI or SERPER API key in .env")

CHATLOG_PATH = Path("Data/Chatlog.json")
CHATLOG_PATH.parent.mkdir(exist_ok=True)

SYSTEM_PROMPT = f"""
You are {ASSISTANT_NAME}, an information extraction engine.

MODE: STRICT EXTRACTION AND PHRASING ONLY

Rules (mandatory):
- You may ONLY use facts explicitly present in the provided web context.
- You may NOT infer, assume, estimate, or complete missing information.
- If required facts are missing, respond exactly with:
  "Realtime data unavailable."
- Rephrase extracted facts into clear English.
- Do NOT add units, dates, conditions, or descriptors unless stated.
- Maximum 2 sentences, but witty like J.A.R.V.I.S .
- No lists. No explanations. No meta text.
""".strip()


class ChatMemory:
    def __init__(self, path: Path):
        self.path = path
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def load(self):
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

    def append(self, role: str, content: str):
        data = self.load()
        data.append({"role": role, "content": content})
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")


memory = ChatMemory(CHATLOG_PATH)


def realtime_search(query: str) -> str:
    conn = http.client.HTTPSConnection("google.serper.dev")

    payload = json.dumps({
        "q": query,
        "num": 3
    })

    headers = {
        "X-API-KEY": SERPER_KEY,
        "Content-Type": "application/json"
    }

    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    raw_data = res.read().decode("utf-8")
    data = json.loads(raw_data)

    snippets = []
    for item in data.get("organic", [])[:3]:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        if title and snippet:
            snippets.append(f"{title}: {snippet}")

    return "Verified realtime web context:\n" + "\n".join(snippets)


def time_context() -> str:
    now = datetime.datetime.now()
    return (
        f"Current date and time:\n"
        f"{now.strftime('%A, %d %B %Y, %H:%M:%S')}"
    )


client = genai.Client(api_key=GEMINI_KEY)


def generate_response(user_prompt: str) -> str:
    web_context = realtime_search(user_prompt)

    contents = f"""
{SYSTEM_PROMPT}

BEGIN VERIFIED WEB CONTEXT
{web_context}
END VERIFIED WEB CONTEXT

User question:
{user_prompt}
""".strip()


    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents
    )

    return response.text.strip().replace("</s>", "")


def process_query(prompt: str) -> str:
    answer = generate_response(prompt)

    memory.append("user", prompt)
    memory.append("assistant", answer)

    return answer


if __name__ == "__main__":
    print(f"{ASSISTANT_NAME} online. Awaiting input.\n")

    while True:
        try:
            user_input = input("Enter your query: ").strip()
            if not user_input:
                continue

            reply = process_query(user_input)
            print(reply + "\n")

        except KeyboardInterrupt:
            print("\nSession terminated.")
            break
