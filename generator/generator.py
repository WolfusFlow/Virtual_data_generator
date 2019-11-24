import os
import json
import datetime as dt
import pika
import time
import random
import uuid

ROUTING_KEY = os.environ['ROUTING_KEY']
SERVER_NAME = os.environ['SERVER_NAME']
AMPQ_URL    = os.environ['AMQP_URL']
TYPE_LIST   = ['A_type', 'B_type', 'C_type']


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMPQ_URL))
        channel = connection.channel()
        while True:
            time_for_sleep = generate_data(channel)
            print(time_for_sleep)
            if time_for_sleep == TYPE_LIST[0]:
                time.sleep(2)
            elif time_for_sleep == TYPE_LIST[-1]:
                time.sleep(4)
            else:
                time.sleep(6)

    except (Exception, pika.exceptions.AMQPConnectionError) as error:
        print(f'error in mq generator connection: {error}')


def send_message(channel, data):
    # mb add a bit of delay / freeze and check delay_channel later
    try:
        channel.basic_publish(exchange='',
                          routing_key=ROUTING_KEY, 
                          body=json.dumps(data))
    except Exception as error:
        print(f'error on send to mq: {error}')


def generate_data(channel):
    created_at = str(dt.datetime.now()).split('.')[0]
    data_type = random.choice(TYPE_LIST)
    value = random.randrange(0, 12000, 125)
    id_field = str(uuid.uuid1())
    data = {
        'data_id' : id_field,
        'data_type' : data_type,
        'value' : value,
        'created_at' : created_at,
        'server_name' : SERVER_NAME
    }
    send_message(channel, data)
    return data_type


if __name__ == '__main__':
    main()