import pygame
import random
import asyncio
import edge_tts
import os
import time
from dotenv import dotenv_values

# ===================== ENV =====================
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-IN-NeerjaNeural")

AUDIO_PATH = os.path.join("Data", "speech.mp3")
os.makedirs("Data", exist_ok=True)

# ===================== CORE TTS LOGIC =====================
async def _save_audio(text: str):
    """Internal async function to save TTS to file."""
    communicate = edge_tts.Communicate(
        text=text,
        voice=AssistantVoice,
        pitch="+5Hz",
        rate="+13%"
    )
    await communicate.save(AUDIO_PATH)

def TTS(text: str, should_continue=lambda: True):
    try:
        # Crucial: Unload the mixer to release the file lock on speech.mp3
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Generate new audio file
        asyncio.run(_save_audio(text))

        # Play the new file
        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            if not should_continue():
                pygame.mixer.music.stop()
                break
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"[TTS ERROR]: {e}")

# ===================== SMART TEXT SPLIT =====================
def TextToSpeech(text: str, should_continue=lambda: True):
    responses = [
        "The rest of the answer is available on the chat screen, sir.",
        "Please check the chat screen for the remaining details, sir.",
        "You'll find the full response on the chat screen, sir."
    ]

    if len(text) > 250:
        # Take first two sentences
        sentences = text.split(". ")
        spoken = ". ".join(sentences[:2]) + ". " + random.choice(responses)
        TTS(spoken, should_continue)
    else:
        TTS(text, should_continue)

# ===================== MAIN =====================
if __name__ == "__main__":
    pygame.mixer.init()
    try:
        while True:
            user_input = input("Enter the Text (or 'quit' to exit): ")
            if user_input.lower() == 'quit':
                break
            TextToSpeech(user_input)
    finally:
        pygame.mixer.quit()