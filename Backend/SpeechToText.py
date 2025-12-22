from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import mtranslate as mt
import os
import time
import atexit

# ===================== ENV =====================
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage", "en-IN")

BASE_DIR = os.getcwd()
HTML_PATH = os.path.join(BASE_DIR, "Data", "Voice.html")
STATUS_PATH = os.path.join(BASE_DIR, "Frontend", "Files", "Status.data")

os.makedirs(os.path.dirname(HTML_PATH), exist_ok=True)
os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)

# ===================== HTML + JS =====================
HTMLCode = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Jarvis Speech Recognition</title>
</head>
<body>

<button id="start">Start</button>
<button id="end">Stop</button>
<p id="output"></p>

<script>
let recognition;
const output = document.getElementById("output");

document.getElementById("start").onclick = () => {{
    recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "{InputLanguage}";
    recognition.continuous = true;

    recognition.onresult = (event) => {{
        const transcript = event.results[event.results.length - 1][0].transcript;
        output.textContent += transcript;
    }};

    recognition.start();
}};

document.getElementById("end").onclick = () => {{
    if (recognition) {{
        recognition.stop();
    }}
}};
</script>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(HTMLCode)

# ===================== CHROME SETUP =====================
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
atexit.register(driver.quit)

# ===================== UTILS =====================
def SetAssistantStatus(status: str):
    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        f.write(status)

def QueryModifier(query: str) -> str:
    query = query.strip().lower()
    if not query:
        return ""
    if query[-1] not in ".?!":
        query += "?"
    return query

def UniversalTranslator(text: str) -> str:
    translated = mt.translate(text, "en", "auto")
    return translated.capitalize()

# ===================== SPEECH RECOGNITION =====================
def SpeechRecognition(timeout: int = 30) -> str:
    driver.get("file:///" + HTML_PATH)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.ID, "start"))).click()

    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            text = driver.find_element(By.ID, "output").text.strip()

            if text:
                driver.find_element(By.ID, "end").click()

                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(text))

            time.sleep(0.3)

        except Exception:
            time.sleep(0.5)

    return ""


if __name__ == "__main__":
    while True:
        result = SpeechRecognition()
        if result:
            print("Jarvis Heard:", result)
