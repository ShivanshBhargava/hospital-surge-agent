# src/llm_setup.py
from google import genai
from .config import GEMINI_API_KEY

_client = None

def configure_genai():
    """Configure a single global Gemini client for the whole app."""
    global _client

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in .env")

    if _client is None:
        _client = genai.Client(api_key=GEMINI_API_KEY)

    return _client

def get_client():
    """Return the configured Gemini client."""
    if _client is None:
        raise RuntimeError("configure_genai() must be called before using Gemini client")
    return _client
