import logging
from uuid import uuid4

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_PAUSED, STATE_STOPPED
from apscheduler.triggers.cron import CronTrigger
from news_scheduler.models.news_job import NewsJob
from news_scheduler.services.news_jobs_runner_service import NewsJobRunnerService

logger = logging.getLogger(__name__)


class NewsJobSchedulerService:
    def __init__(self, jobs: list[NewsJob], runner: NewsJobRunnerService):
        self.jobs = jobs
        self.runner = runner
        self._scheduler = BackgroundScheduler()

        for job in self.jobs:
            self.add_job(job)

    def add_job(self, job: NewsJob):
        logger.info(f"Adding news job: {job.id}")
        self._scheduler.add_job(
            func=self.runner.run_job,
            kwargs={"job": job},
            trigger=CronTrigger(minute="*", second=0),
        )

    def start(self):
        if (
            self._scheduler.state == STATE_STOPPED
            or self._scheduler.state == STATE_PAUSED
        ):
            self._scheduler.start()

    def shutdown(self):
        if self._scheduler.state != STATE_STOPPED:
            self._scheduler.shutdown()
