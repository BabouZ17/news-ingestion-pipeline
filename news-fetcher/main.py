from news_fetcher.connectors.http_connector import HTTPConnector
from news_fetcher.fetchers.http_fecther import HTTPFetcher
from news_fetcher.parsers.json_parser import JSONParser

if __name__ == "__main__":
    http_connector = HTTPConnector()
    http_fetcher = HTTPFetcher(
        url="http://localhost:8000/api/news", connector=http_connector
    )
    json_parser = JSONParser()

    data = http_fetcher.fetch()
    print(data)

    news = json_parser.parse(data)
    print(news)
