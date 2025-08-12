from fastapi import APIRouter, FastAPI
from news_api.routes.home import home
from news_api.routes.index import create_index
from news_api.routes.news import (
    add_news,
    count_news,
    delete_news,
    get_news,
    hybrid_search_news,
    keyword_search_news,
    semantic_search_news,
)

home_router = APIRouter()
home_router.add_api_route("/", home)

news_router = APIRouter(prefix="/api/news")
news_router.add_api_route("/", get_news)
news_router.add_api_route("/", add_news, methods=["POST"])
news_router.add_api_route("/", delete_news, methods=["DELETE"])

news_router.add_api_route("/keywordSearch", keyword_search_news)
news_router.add_api_route("/hybridSearch", hybrid_search_news)
news_router.add_api_route("/semanticSearch", semantic_search_news)
news_router.add_api_route("/count", count_news)
news_router.add_api_route("/createIndex", create_index)

test_router = APIRouter()
test_router.add_api_route("/ingest", add_news, methods=["POST"])
test_router.add_api_route("/retrieve", hybrid_search_news)

app = FastAPI()
app.include_router(home_router)
app.include_router(news_router)
app.include_router(test_router)
