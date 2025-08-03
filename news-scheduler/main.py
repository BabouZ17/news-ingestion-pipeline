import os
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter, FastAPI
from news_scheduler.connectors.kafka_producer import KafkaProducer
from news_scheduler.routes.home import home

TOPIC = os.getenv("TOPIC")
assert TOPIC is not None, "Invalid topic given"

BOOTSTRAP_SERVERS = os.environ["BOOTSTRAP_SERVERS"]
assert BOOTSTRAP_SERVERS is not None, "Invalid boostrap servers given"

kafka_producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS], topic=TOPIC)


def test(producer: KafkaProducer):
    producer.send(key="test", value=f"im a test: {datetime.now()}")


scheduler = BackgroundScheduler()
scheduler.add_job(
    func=test, kwargs={"producer": kafka_producer}, trigger=CronTrigger(second="*/10")
)
scheduler.start()

home_router = APIRouter()
home_router.add_api_route("/", home)

app = FastAPI()
app.include_router(home_router)
