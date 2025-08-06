import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from config import GEMINI_API_KEY

load_dotenv()

API_KEY = GEMINI_API_KEY
if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing. Check GitHub Secrets or .env")
# Create a shared Gemini chat model instance
chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
    google_api_key=API_KEY
)

def refine_prompt(base_prompt: str) -> str:
    """
    Improves an image generation prompt using Gemini via LangChain.
    """
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a creative AI prompt engineer. Make the prompt vivid, detailed, and visually engaging. Include art style, lighting, and composition. Keep it under 50 words."),
        ("human", "{prompt}")
    ])
    chain = template | chat_model
    result = chain.invoke({"prompt": base_prompt})
    return result.content.strip()

def refine_caption_for_post(image_prompt: str) -> str:
    """
    Creates ONE Instagram caption based on the exact refined image description.
    """
    template = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a witty and engaging Instagram caption writer. "
            "Write ONE short caption for an image described below. "
            "The caption MUST directly match the image description. "
            "It can be funny, sarcastic, or inspirational depending on the mood of the scene. "
            "Include 5-10 relevant hashtags. Output ONLY the caption."
        ),
        ("human", "{image_prompt}")
    ])
    chain = template | chat_model
    result = chain.invoke({"image_prompt": image_prompt})
    return result.content.strip()

    
def generate_daily_prompt(subject: str) -> str:
    """
    Given a subject, generate a unique AI image prompt for today.
    """
    template = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a creative AI image prompt writer. "
         "Generate ONE unique, vivid, and detailed image idea related to the given subject. "
         "Avoid repeating past ideas. No text in image. Include art style, lighting, and composition. "
         "Keep under 50 words."
        ),
        ("human", "{subject}")
    ])
    chain = template | chat_model
    result = chain.invoke({"subject": subject})
    return result.content.strip()




