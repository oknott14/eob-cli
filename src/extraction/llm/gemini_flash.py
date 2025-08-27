from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI


class GoogleGeminiFlash(ChatGoogleGenerativeAI):
    def __init__(self, **kwargs: Any):
        kwargs["model"] = "gemini-2.0-flash"
        super().__init__(**kwargs)
