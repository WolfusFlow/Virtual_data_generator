import os
import json
import datetime as dt
import pika
import time
import random

ROUTING_KEY = os.environ['ROUTING_KEY']
SERVER_NAME = os.environ['SERVER_NAME']
AMPQ_URL    = os.environ['AMQP_URL']
TYPE_LIST   = ['A_type', 'B_type', 'C_type']


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMPQ_URL))
        channel = connection.channel()
        generate_data(channel)

    except (Exception, pika.exceptions.AMQPConnectionError) as error:
        print(f'error in mq generator connection: {error}')


def send_message(channel, data):
    # mb add a bit of delay / freeze and check delay_channel later
    channel.basic_publish(exchange='',
                      routing_key=ROUTING_KEY, 
                      body=json.dumps({'data_type' : data.get('data_type'),
                                       'value' : data.get('value'), 
                                       'created_at': data.get('created_at'), 
                                       'server_name': data.get('server_name')}))
    

def generate_data(channel):
    while True:
        created_at = str(dt.datetime.now()).split('.')[0]
        data_type = random.choice(TYPE_LIST)
        value = random.randrange(0, 12000, 125)
        data = {
            'data_type' : data_type,
            'value' : value,
            'created_at' : created_at,
            'server_name' : SERVER_NAME
        }
        send_message(channel, data)

if __name__ == '__main__':
    main()