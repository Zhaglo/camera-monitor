import asyncio

import aio_pika


async def main():
    connection = await aio_pika.connect(
        'amqp://student:learning@127.0.0.1:5672/',
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('learning', durable=True)

        message = aio_pika.Message(
            body='Привет из Python'.encode('utf-8'),
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )
        print(f'Сообщение опубликовано в очередь {queue.name}')


if __name__ == '__main__':
    asyncio.run(main())