import os

GPT_API_KEY = os.getenv("GPT_API_KEY", "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")

# Application settings
APP_NAME = "Education Chatbot"
APP_VERSION = "1.0.0"
DEFAULT_LANGUAGE = "en" 

# Debug mode
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
