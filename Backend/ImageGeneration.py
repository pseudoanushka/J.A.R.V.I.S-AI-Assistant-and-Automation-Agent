import asyncio
import os
from PIL import Image
from dotenv import get_key
from huggingface_hub import InferenceClient
from time import sleep

# --- Configuration ---
if not os.path.exists("Data"):
    os.makedirs("Data")

# Initialize the official Hugging Face Client
# It automatically finds the correct URL and handles authentication
HF_TOKEN = get_key('.env', 'HuggingFace')
client = InferenceClient(api_key=HF_TOKEN)

# --- Functions ---

def open_image(prompt):
    """Opens the first generated image for the given prompt."""
    safe_prompt = prompt.replace(" ", "_")
    image_path = os.path.join("Data", f"{safe_prompt}1.jpg")

    try:
        if os.path.exists(image_path):
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
        else:
            print(f"File not found: {image_path}")
    except Exception as e:
        print(f"Unable to open {image_path}: {e}")

async def generate_images(prompt: str):
    """Generates images using the official InferenceClient."""
    safe_prompt = prompt.replace(" ", "_")
    
    print(f"Requesting images for: {prompt}...")

    # We run the client in a thread to keep it from blocking the event loop
    def call_client():
        return client.text_to_image(
            prompt=f"{prompt}, quality=4K, ultra high details",
            model="stabilityai/stable-diffusion-xl-base-1.0"
        )

    try:
        # Generate 1 images
        for i in range(1, 2):
            # The client returns a PIL Image object directly
            image = await asyncio.to_thread(call_client)
            
            file_path = os.path.join("Data", f"{safe_prompt}{i}.jpg")
            image.save(file_path)
            print(f"Successfully saved: {file_path}")
            
    except Exception as e:
        print(f"Generation failed: {e}")

def GenerateImages(prompt: str):
    """Wrapper to run the async generation and open the result."""
    asyncio.run(generate_images(prompt))
    open_image(prompt)

# --- Main Loop ---

print("System Active. Monitoring ImageGeneration.data...")

while True:
    data_file = os.path.join("Frontend", "Files", "ImageGeneration.data")
    
    try:
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                content = f.read().strip()
            
            if content and "," in content:
                prompt, status = content.split(",")
                
                if status.strip() == "True":
                    print(f"\n--- Signal Received: {prompt} ---")
                    GenerateImages(prompt=prompt)

                    # Reset the file status
                    with open(data_file, "w") as f:
                        f.write("False,False")
                    print("--- Resetting Trigger ---")
        
        sleep(1) 
    except Exception as e:
        print(f"Loop Error: {e}")
        sleep(2)