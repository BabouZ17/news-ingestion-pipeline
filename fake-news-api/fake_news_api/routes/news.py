from datetime import datetime

from fake_news_api.models.news import News

NEWS: list[News] = [
    News(
        author="dummy_one",
        content="I am a dummy news",
        posted_at=datetime(year=2025, month=1, day=1),
    ),
    News(
        author="dummy_two",
        content="I am another dummy news",
        posted_at=datetime(year=2025, month=2, day=2),
    ),
]


def get_news() -> list[News]:
    """Return a list of fake news"""
    return NEWS
