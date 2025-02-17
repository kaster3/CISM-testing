import os

from taskiq import AsyncBroker, InMemoryBroker
from taskiq_aio_pika import AioPikaBroker

from core.settings import settings

env = os.environ.get("ENVIRONMENT")

broker: AsyncBroker = AioPikaBroker(
    url=settings.rabbitmq.url,
)

if env and env == "pytest":
    broker = InMemoryBroker()
