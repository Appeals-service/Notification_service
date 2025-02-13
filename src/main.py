import asyncio
import json
import logging

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage

from src.send_mail import send_message
from src.settings import settings

logger = logging.getLogger(__name__)
logging.basicConfig(format=settings.LOGGING_FORMAT)
logger.setLevel(settings.LOGGING_LEVEL)


async def process_message(message: AbstractIncomingMessage) -> None:
    logger.info("Message received")
    async with message.process():
        message = json.loads(message.body)

        if  not (email := message.pop("email")) or not message:
            raise ValueError("Incorrect data")

        await send_message(email, json.dumps(message))


async def main() -> None:
    connection = await connect_robust(settings.get_rmq_url())
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(settings.RABBITMQ_QUEUE_NAME)

    await queue.consume(process_message)
    logger.info("Waiting for messages...")

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())