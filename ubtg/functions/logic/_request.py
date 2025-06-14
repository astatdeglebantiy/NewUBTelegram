import requests


def _function(url: str, method: str = 'GET', headers: dict | None = None, data: dict | None = None, json: dict | None = None) -> dict:
    headers = headers or {}
    data = data or {}
    json = json or {}

    try:
        response = requests.request(method, url, headers=headers, data=data, json=json)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}") from e
