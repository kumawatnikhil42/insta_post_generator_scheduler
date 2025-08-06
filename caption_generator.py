import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def generate_caption(image_prompt: str):
    """
    Generates ONE Instagram caption based on the given image description.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    
    prompt = f"""
    You are a witty and creative Instagram caption writer.
    Write ONE short caption for the image described below:
    {image_prompt}

    Rules:
    - Keep it under 15 words.
    - Must clearly relate to the scene.
    - Use emojis naturally if needed.
    - Add 8-10 relevant hashtags.
    - Output ONLY the caption text, no explanations.
    """

    result = llm.invoke(prompt)
    return result.content.strip()
