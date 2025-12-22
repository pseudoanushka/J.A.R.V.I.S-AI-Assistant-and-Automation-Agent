from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search,playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from google import genai
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars = dotenv_values(".env")

GEMINIAPIKey = env_vars.get("GEMINIAPIKey")
SYSTEM_PROMPT = """Just give one response, not much text content you have to be super accurate like you have been writing contents since years " \
for sick 
FewShotExamples = [
    # Example 1: WhatsApp Message
    {"role": "user", "content": "Write a WhatsApp message to my manager about being late due to traffic."},
    {"role": "model", "content": "Subject: Delay Notification\n\nGood morning, Sir. I’m currently delayed by an unusual congestion on the main arterial route. I anticipate arriving approximately 20 minutes behind schedule. My apologies for the inconvenience; I shall resume my duties the moment I reach the office."},

    # Example 2: Official Email
    {"role": "user", "content": "Write an email to a client requesting a meeting for project feedback."},
    {"role": "model", "content": "Subject: Request for Project Review Meeting - [Project Name]\n\nDear [Client Name],\n\nI hope this find you well. As we have reached a significant milestone in our current phase, I would appreciate the opportunity to discuss your feedback and ensure our trajectory aligns with your expectations.\n\nWould you be available for a brief call this Thursday at 2:00 PM? I look forward to your thoughts.\n\nBest regards,\n[Your Name]"},

    # Example 3: Application Letter
    {"role": "user", "content": "Write a short leave application for a dental appointment."},
    {"role": "model", "content": "Subject: Leave Application - Dental Procedure\n\nTo the HR Department,\n\nI am writing to formally request a half-day leave of absence on [Date], starting from 1:00 PM, to attend a confirmed dental appointment. I have ensured that my current tasks are up to date to prevent any disruption in my absence. Thank you for your consideration.\n\nSincerely,\n[Your Name]"}
]

"""
classes = [
    "zrubwfm",
    "hgkEle",
    "LTKOO",
    "sY7ric",
    "gsrt",
    "vk_bk",
    "FzVN5b",
    "Yiehnf",
    "tw-Data-text",
    "tw-text-small",
    "tw-ta",
    "176rdc",
    "05uR6d",
    "LTKO0",
    "evlzY6d",
    "webanswers-webanswers_table_webanswers-table",
    "dDoNo",
    "ikb4Bb",
    "snaDes",
    "LWRfKe",
    "VQF4g",
    "qv3Wpes",
    "kno-rdesc",
    "5PZz6b1"
]
useragent = "Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,like Gecko)Chrome/100.0.4896.75 Safari/537.36"
client = genai.Client(api_key=GEMINIAPIKey)

professional_responses = [
    "I've anticipated a few follow-up queries regarding this data. Shall I present the projections?",
        "All systems are nominal. Would you like me to cross-reference this with your previous archives?",
        "The connection is stable. I'm ready to push these parameters to the main frame if you're satisfied."
    ]
messages = []

SystemChatbot = [
    {"role":"system","content":f"Hello, I am {os.environ['Username']},You're a content writer,You have to write content like letter, email, or frame whatsapp messages as per the instructions and requirements"}
]

def GoogleSearch(Topic):
    search(Topic) #use Pywhatkit to perform search operation
    return True
#Function to generate content using AI and to save it
# --- REPAIRED FUNCTIONS ---

def ContentWriterAI(prompt):
    # Use the client you initialized at the top of your script
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"{SYSTEM_PROMPT}{prompt}".strip(),
            config={
                "temperature": 0.7,
                "max_output_tokens": 2048,
            }
        )
        Answer = response.text
        # Optional: Append to history if you want JARVIS to remember
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "model", "content": Answer})
        return Answer
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm sorry, sir, I encountered an error while writing the content."

def Content(Topic):
    os.makedirs("Data", exist_ok=True)

    def OpenNotepad(File):
        if os.path.exists(File):
            subprocess.Popen(["notepad.exe", File])

    # Clean the input
    query = Topic.lower().replace("content", "").strip()
    print(f"Generating content for: {query}...")

    # Call the AI
    result = ContentWriterAI(query)

    # Save and Open
    filename = f"{query.replace(' ', '_')}.txt"
    file_path = os.path.join("Data", filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(result)
    
    OpenNotepad(file_path)
    return True

# --- EXECUTION ---

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"    
    webbrowser.open(Url4Search)
    return True
# YoutubeSearch("Play bye bye by deadpool")
def PlayYoutube(query):
    playonyt(query) #application of pywhakit
    return True
def OpenApp(app,sess =requests.session()):
    try:
        appopen(app,match_closest=True,output=True,throw_error=True) #attempt to open the app
        return True
    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html,'html.parser')
            links = soup.find_all('a',{'jsname':'UWckNb'})
            return [link.get('href') for link in links]
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent":useragent}
            response = sess.get(url,headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve google results")
            return None
        html = search_google(app) #perform google search

        if html:
            link = extract_links(html[0])
            webopen(link)
        return True
# OpenApp("camera")   
#for closing an application
def CloseApp(app):
    if"chrome" in app:
        pass
    else:
        try:
            close(app,match_closest=True,output=True,throw_error=True)
            return True
        except:
            return False
# CloseApp("settings")        
def System(command):
    #nested function to make the system mute
    def mute():
        keyboard.press_and_release("volume mute") 
    def unmute():
        keyboard.press_and_release("volume unmute")
    def volumeup():
        keyboard.press_and_release("volume up") 
    def volumedown():
        keyboard.press_and_release("volume down")
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volumeup()
    elif command == "volume down":
        volumedown()
    return True
async def TranslateAndExecute(commands:list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "): #handles open command
            if "open it " in command:
                pass
            if "open file" == command:
                pass 
            else:
                fun = asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "): #placeholder for general command
            pass
        elif command.startswith("realtime "):    #placeholder for realtime command
            pass
        elif command.startswith("close"):    #handles close command
            fun = asyncio.thread(CloseApp,command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube,command.removeprefix("play")) #Schedule youtube playback
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content,command.removeprefix("content"))
            funcs.append(fun)
        elif command.startswith("google search"):
            fun = asyncio.to_thread(GoogleSearch,command.removeprefix("google search"))
            funcs.append(fun)
        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(YoutubeSearch,command.removeprefix("youtube")) 
            funcs.append(fun)
        elif command.startswith("system"):
            fun = asyncio.to_thread(YoutubeSearch,command.removeprefix("system"))    
            funcs.append(fun)
        else:
            print(f"No functions found, for {command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        if isinstance(results,str):
            yield result
async def Automation(commands:list[str]):
    async for result in TranslateAndExecute(commands): #Translate and execute commands
        pass
    return True
if __name__ == "__main__":
    asyncio.run(Automation(["open instagram","play Despacito","open camera","content whatsapp message for me to ask for notes to my friend","open settings"]))









