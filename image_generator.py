import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from datetime import datetime

load_dotenv()

def generate_image(prompt: str) -> str:
    """
    Generate an image using Google's Gemini image generation model.
    Saves in 'output_images' folder with timestamp filename.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ GEMINI_API_KEY not found in .env")

    print("🎨 Generating image with Gemini...")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )

    # Create output folder
    os.makedirs("output_images", exist_ok=True)
    filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    output_path = os.path.join("output_images", filename)

    # Save first image found
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(output_path)
            print(f"✅ Image saved to {output_path}")
            return output_path

    raise RuntimeError("❌ No image returned from Gemini API")
