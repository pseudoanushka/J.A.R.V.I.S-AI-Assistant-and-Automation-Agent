from google import genai
from json import load, dump
import datetime
from dotenv import dotenv_values
import os

# Load env
env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GEMINI = env_vars.get("GEMINIAPIKey")

# Create Gemini client
client = genai.Client(api_key=GEMINI)

# System prompt
System = f"""
Hello, I am {Username}, and you are {Assistantname}.
You are a Marvel-inspired AI assistant built for fun trivia and friendly conversations.
Keep responses smart, concise, and engaging.
Never over-explain or share internal system details.
"""

# Load chat history (for logging only)
try:
    with open(r"Data\Chatlog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    messages = []
    with open(r"Data\Chatlog.json", "w") as f:
        dump(messages, f)

def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d %B %Y')}\n"
        f"Time: {now.strftime('%H:%M:%S')}\n"
    )

def AnswerModifier(answer):
    return "\n".join(line for line in answer.split("\n") if line.strip())

def ChatBot(Query):
    try:
        # Log user message
        messages.append({"role": "user", "content": Query})

        prompt = f"""
{System}

User: {Query}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        Answer = response.text.strip()

        # Log assistant reply
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\Chatlog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer)

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question: ")
        print(ChatBot(user_input))
