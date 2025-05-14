from google.genai.types import GenerateContentConfig
import config
from google import genai

GEMINI_API_KEY = config.load(config.API_KEYS_PATH)['GEMINI_API']


def generate_content(prompt: str | None = None, system_prompt: str | None = None, media: list[str] | None = None, model: str = 'gemini-2.0-flash', temperature: int = 1, api_key: str = GEMINI_API_KEY):
    if (not prompt) and (not media):
        raise ValueError('No "prompt" or "images" provided')

    generation_config = GenerateContentConfig(
        temperature=temperature,
        system_instruction=system_prompt
    )

    client = genai.Client(api_key=api_key)
    new_media = []
    if type(media) == list:
        for m in media:
            new_media.append(client.files.upload(file=m))
    if new_media:
        content = client.models.generate_content(model=model, contents=[prompt, *new_media], config=generation_config)
    else:
        content = client.models.generate_content(model=model, contents=[prompt], config=generation_config)
    return content
