import asyncio

import aio_pika

from schemas import CheckJob


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
                    job = CheckJob.model_validate_json(message.body)
                    print('ID задания:', job.check_id)
                    print('Список адресов:', job.urls)
                    print('Время таймаута:', job.timeout)


if __name__ == '__main__':
    asyncio.run(main())