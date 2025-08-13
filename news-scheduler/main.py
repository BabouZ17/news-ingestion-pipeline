import os
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from news_scheduler.config.config import Config
from news_scheduler.connectors.kafka_producer_connector import KafkaProducerConnector
from news_scheduler.routes.home import home
from news_scheduler.routes.jobs import run_job
from news_scheduler.services.news_jobs_runner_service import NewsJobRunnerService
from news_scheduler.services.news_jobs_scheduler_service import (
    NewsJob,
    NewsJobSchedulerService,
)


def build_app() -> FastAPI:
    jobs = [NewsJob(name="fake-news-api", url="http://fake-news-api:8000/api/news")]
    config = Config()

    kafka_producer = KafkaProducerConnector(
        topic=config.topic, bootstrap_servers=[config.bootstrap_servers]
    )
    runner_service = NewsJobRunnerService(kafka_producer)
    news_jobs_scheduler = NewsJobSchedulerService(jobs=jobs, runner=runner_service)

    home_router = APIRouter()
    home_router.add_api_route("/", home)

    jobs_router = APIRouter(prefix="/jobs")
    jobs_router.add_api_route("/run_job", run_job, methods=["POST"])

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        news_jobs_scheduler.start()
        yield
        news_jobs_scheduler.shutdown()

    app = FastAPI(lifespan=lifespan)
    app.include_router(home_router)
    app.include_router(jobs_router)

    return app


app = build_app()
