from typing import Annotated

from fastapi import Depends
from news_scheduler.models.news_job import NewsJob
from news_scheduler.services.news_jobs_runner_service import (
    NewsJobRunnerService,
    get_news_job_runner_service,
)


async def run_job(
    job: NewsJob,
    runner: Annotated[NewsJobRunnerService, Depends(get_news_job_runner_service)],
):
    runner.run_job(job)
