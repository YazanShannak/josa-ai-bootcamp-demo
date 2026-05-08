import os
from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

load_dotenv()

_openrouter_client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def get_model(model_name: str = "openai/gpt-4o") -> OpenAIModel:
    return OpenAIModel(
        model_name,
        provider=OpenAIProvider(openai_client=_openrouter_client),
    )
