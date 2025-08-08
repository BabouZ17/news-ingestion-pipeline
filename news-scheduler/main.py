import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from news_scheduler.connectors.kafka_producer_connector import KafkaProducerConnector
from news_scheduler.routes.home import home
from news_scheduler.services.news_jobs_scheduler import NewsJob, NewsJobScheduler


def build_app() -> FastAPI:
    TOPIC = os.getenv("TOPIC")
    assert TOPIC is not None, "Invalid topic given"

    BOOTSTRAP_SERVERS = os.environ["BOOTSTRAP_SERVERS"]
    assert BOOTSTRAP_SERVERS is not None, "Invalid boostrap servers given"

    kafka_producer_connector = KafkaProducerConnector(
        bootstrap_servers=[BOOTSTRAP_SERVERS], topic=TOPIC
    )

    jobs = [NewsJob(name="fake-news-api", url="http://fake-news-api:8000")]
    news_jobs_scheduler = NewsJobScheduler(
        jobs=jobs, producer_connector=kafka_producer_connector
    )

    home_router = APIRouter()
    home_router.add_api_route("/", home)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        news_jobs_scheduler.start()
        yield
        news_jobs_scheduler.shutdown()

    app = FastAPI(lifespan=lifespan)
    app.include_router(home_router)

    return app


app = build_app()
