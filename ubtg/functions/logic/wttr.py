import requests


def _function(city: str | None = None, _format: int = 4) -> str:
    return requests.get(f"https://wttr.in/{city if city else ''}?format={_format}").text