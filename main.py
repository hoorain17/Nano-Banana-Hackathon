import os
from google import genai
from PIL import Image
from io import BytesIO

# --- Load API Key ---
# It's recommended to use environment variable
API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyCCGkBDbMzmXNlV59D1e6jmR2uzBQEG-_4"

# Configure the client
client = genai.Client(api_key=API_KEY)

# Directory to save generated images
OUTPUT_DIR = "output/scenes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load prompts from file
with open("prompts/scene_prompts.txt", "r", encoding="utf-8") as f:
    prompts = [line.strip() for line in f if line.strip()]

for i, prompt in enumerate(prompts, start=1):
    print(f"Generating Scene {i}...")
    
    try:
        # Call the Gemini model
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=prompt
        )

        # Extract image data
        image_parts = [
            part.inline_data.data
            for part in response.candidates[0].content.parts
            if part.inline_data
        ]

        if image_parts:
            image = Image.open(BytesIO(image_parts[0]))
            filename = f"{OUTPUT_DIR}/scene_{i}.png"
            image.save(filename)
            print(f"Scene {i} saved to {filename}")
        else:
            print(f"No image generated for Scene {i}")

    except Exception as e:
        print(f"Error generating Scene {i}: {e}")
