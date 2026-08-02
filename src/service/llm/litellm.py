from litellm import acompletion
from config.settings import settings

async def get_completion(messages: list[dict], model: str = "openrouter/openai/gpt-4o", stop=[]) -> str:
    return await acompletion(model=model, messages=messages, api_key=settings.OPENROUTER_API_KEY, max_tokens=1500, temperature=0, stop=stop)