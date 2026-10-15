from uuid import uuid4

import asyncio

import aio_pika

from schemas import CheckJob


async def main():
    job = CheckJob(
        check_id=uuid4(),
        urls=['http://127.0.0.1:8002/state'],
        timeout=3,
    )

    connection = await aio_pika.connect(
        'amqp://student:learning@127.0.0.1:5672/',
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('learning', durable=True)

        message = aio_pika.Message(
            body=job.model_dump_json().encode('utf-8'),
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )
        print(f'Сообщение опубликовано в очередь {queue.name}')


if __name__ == '__main__':
    asyncio.run(main())