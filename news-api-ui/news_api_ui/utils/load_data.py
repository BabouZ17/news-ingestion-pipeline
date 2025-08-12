import requests
from typing import Any


def load_data(url: str, path: str, query: str | None = None) -> list[dict[str, Any]]:
    """Simple snippet to fetch news

    Args:
        url (str): Url of the news-api
        path (str): path of the endpoint to hit
        query (str | None): Query to pass
    Returns:
        list[dict[str, Any]]
    Raises:
        HTTPError: When error occured
    """
    full_url = f"{url}/{path}"
    if query is not None:
        full_url += f"?query={query}"

    response = requests.get(url=full_url)
    response.raise_for_status()

    return response.json()
