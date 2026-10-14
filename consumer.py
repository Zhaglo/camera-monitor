import asyncio

import aio_pika


async def main():
    connection = await aio_pika.connect(
        'amqp://student:learning@127.0.0.1:5672/',
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('learning', durable=True)

        async with queue.iterator() as messages:
            async for message in messages:
                async with message.process():
                    print('Получено:', message.body.decode('utf-8'))


if __name__ == '__main__':
    asyncio.run(main())