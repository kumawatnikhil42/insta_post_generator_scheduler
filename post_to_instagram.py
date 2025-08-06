from instagrapi import Client
import os
from dotenv import load_dotenv
from config import IG_USER,IG_PASS

load_dotenv()

def post_image(image_path, caption):
    cl = Client()
    cl.login(IG_USER, IG_PASS)
    cl.photo_upload(image_path, caption)
