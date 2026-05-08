from dotenv import load_dotenv
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

load_dotenv()


def get_model(model_name: str = "deepseek/deepseek-v4-flash") -> OpenRouterModel:
    return OpenRouterModel(model_name, provider=OpenRouterProvider())
