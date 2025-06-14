from ubtg import ai_gemini


def _function(prompt: str | None=None, media: list[str] | None=None, system_prompt: str | None=None, model='gemini-2.0-flash', temperature: float=1.0, prompt_length: int=50):
    text = ''
    if prompt and prompt_length > 0:
        short_prompt = (prompt[:int(prompt_length) - 3] + '...') if len(prompt) > int(prompt_length) else prompt
        text += f'**Prompt:**\n```ᅠ\n{short_prompt}\nᅠ```\n\n'
    text += f'**Answer:**\n{ai_gemini.generate_content(prompt=prompt, media=media, system_prompt=system_prompt, model=model, temperature=temperature).text}'
    return text