from __future__ import annotations

import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv


ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"
LOCAL_ENV = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(ROOT_ENV)
load_dotenv(LOCAL_ENV, override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
else:
    model = None


async def generate_reply(prompt: str) -> str:
    if model is None:
        return "The AI provider is not configured yet. Set GEMINI_API_KEY to enable model responses."

    response = model.generate_content(prompt)
    return response.text
