import asyncio
import json

from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage

from src.settings import settings

async def process_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print(message.body)
        print(json.loads(message.body.decode()).get("email"))
        # await asyncio.sleep(5)
        # print("done")



async def main() -> None:
    connection = await connect_robust(settings.get_rmq_url())
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(settings.RABBITMQ_QUEUE_NAME, auto_delete=True)

    await queue.consume(process_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())