import aio_pika
import os


RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

async def send_to_queue(file_path: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("music_queue")
        await channel.default_exchange.publish(
            aio_pika.Message(body=file_path.encode()),
            routing_key=queue.name
        )