from instagrapi import Client
import os
from dotenv import load_dotenv

load_dotenv()

def post_image(image_path, caption):
    cl = Client()
    cl.login(os.getenv("IG_USER"), os.getenv("IG_PASS"))
    cl.photo_upload(image_path, caption)
