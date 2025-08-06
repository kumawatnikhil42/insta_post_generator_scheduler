from instagrapi import Client
import os
import json
from dotenv import load_dotenv
from config import IG_USER,IG_PASS

load_dotenv()

def post_image(image_path, caption):
    cl = Client()

    # Load session from GitHub secret
    session_data = os.getenv("IG_SESSION")
    if not session_data:
        raise ValueError("❌ IG_SESSION secret is missing.")

    settings_dict = json.loads(session_data)

    cl.set_settings(settings_dict) 
    cl.login(IG_USER, IG_PASS)
    cl.photo_upload(image_path, caption)
