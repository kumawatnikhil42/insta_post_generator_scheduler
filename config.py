# config.py
import os
from dotenv import load_dotenv

# Load local .env if exists (won't affect GitHub Actions)
load_dotenv()

# Centralized API key loading
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
IG_USER = os.getenv("IG_USER")
IG_PASS = os.getenv("IG_PASS")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY is missing. Check .env or GitHub Secrets.")

if not IG_USER or not IG_PASS:
    print("⚠️ IG_USER or IG_PASS is missing. Instagram posting may fail.")
