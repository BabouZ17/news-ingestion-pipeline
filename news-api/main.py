from fastapi import APIRouter, FastAPI
from news_api.routes.home import home
from news_api.routes.news import (
    add_news,
    count_news,
    create_index,
    create_vector_index,
    get_news,
)

home_router = APIRouter()
home_router.add_api_route("/", home)

news_router = APIRouter(prefix="/news")
news_router.add_api_route("/", get_news)
news_router.add_api_route("/", add_news, methods=["POST"])
news_router.add_api_route("/count", count_news)

news_router.add_api_route("/createIndex", create_index)
news_router.add_api_route("/createVectorIndex", create_vector_index)

test_router = APIRouter()
test_router.add_api_route("/ingest", add_news, methods=["POST"])
test_router.add_api_route("/retrieve", get_news)

app = FastAPI()
app.include_router(home_router)
app.include_router(news_router)
app.include_router(test_router)
