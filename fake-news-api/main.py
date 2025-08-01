from fastapi import FastAPI, APIRouter
from fake_news_api.routes.home import home
from fake_news_api.routes.news import get_news

home_router = APIRouter()
home_router.add_api_route("/", home)

news_router = APIRouter()
news_router.add_api_route("/news", get_news)

app = FastAPI()
app.include_router(home_router)
app.include_router(news_router, prefix="/api")