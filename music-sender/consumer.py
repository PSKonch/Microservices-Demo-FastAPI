import aio_pika
import asyncio
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")

async def get_from_queue(message: aio_pika.IncomingMessage):
    async with message.process():
        file_path = message.body.decode()
        print(f"[music-sender] File: {file_path}")

async def start_consume():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(
            "music_queue",
            durable=True
        )
        print("[music-sender] Waiting for message handling")

        await queue.consume(get_from_queue)
        await asyncio.Future()