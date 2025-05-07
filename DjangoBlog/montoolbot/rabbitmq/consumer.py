import asyncio
import time
import os
import pika
import json
from telegram import Bot
from threading import Thread

async_loop = asyncio.new_event_loop()

def start_async_loop():
    asyncio.set_event_loop(async_loop)
    async_loop.run_forever()

Thread(target=start_async_loop, daemon=True).start()

bot = Bot(token=os.getenv("TOKEN"))


def callback(ch, method, properties, body):
    data = json.loads(body)
    if method.routing_key == "user.login":
        print(f"Received event: {method.routing_key}, data: {data}")
        asyncio.run_coroutine_threadsafe(send_message_user_login(data), async_loop)
    elif method.routing_key == "post.created":
        print(f"Received event: {method.routing_key}, data: {data}")
        asyncio.run_coroutine_threadsafe(send_message_post_created(data), async_loop)


async def send_message_post_created(data):
    await bot.send_message(
        chat_id=os.getenv("ADMIN_ID"),
        text=f"The new post with id '{data['post_id']}' was created by user with email '{data['email']}'"
    )


async def send_message_user_login(data):
    await bot.send_message(
        chat_id=os.getenv("ADMIN_ID"),
        text=f"The user '{data['user_name']}' logged in at '{data['login_date_time']}'"
    )


def start_consumer(connection):
    channel = connection.channel()

    channel.exchange_declare(exchange="events", exchange_type="topic")
    channel.queue_declare(queue="tg_notifications")
    channel.queue_bind(exchange="events", queue="tg_notifications", routing_key="post.created")
    channel.queue_bind(exchange="events", queue="tg_notifications", routing_key="user.login")

    channel.basic_consume(queue="tg_notifications", on_message_callback=callback, auto_ack=True)
    print("Waiting for messages...")
    channel.start_consuming()


def wait_for_rabbitmq():
    for _ in range(10):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            return start_consumer(connection)
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ...")
            time.sleep(3)
    raise Exception("Could not connect to RabbitMQ")
