"""Configuration module for the MeXR backend."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")

# LLM Configuration
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0

# Session Configuration
MAX_CHAT_HISTORY = 10  # Keep last 10 messages in chat history
