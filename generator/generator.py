import os
import json
import datetime as dt
import pika
import time
import random
import uuid
import logging

logging.basicConfig(filename=f"generator_{os.environ['SERVER_NAME']}_log_file",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

class Send_to_Rabbit():

    def __init__(self):
        self.ampq_url    = os.environ['AMQP_URL']
        self.routing_key = os.environ['ROUTING_KEY']

    mq_connection = None
    mq_channel = None
    

    def connect_to_rabbit(self):
        try:
            self.mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.ampq_url))

            if self.mq_connection.is_open:
                self.mq_channel = self.mq_connection.channel()
                self.mq_channel.queue_declare(queue=self.routing_key, durable=True)

        except pika.exceptions.AMQPConnectionError as error:
            logging.exception(f'Error in AMQP connection: {error}')


    def send_message_to_queue(self, data):
        try:
            self.mq_channel.basic_publish(exchange='',
                                          routing_key=self.routing_key,
                                          body=json.dumps(data),)
            self.mq_connection.close()
        
        except pika.exceptions.ChannelError as error:
            logging.exception(f'error with channel on message send: {error}')


class Message():

    def __init__(self):
        self.type_list = ['A_type', 'B_type', 'C_type']

    def generate_message(self):
        created_at = str(dt.datetime.now()).split('.')[0]
        data_type = random.choice(self.type_list)
        value = random.randrange(0, 12000, 125)
        id_field = str(uuid.uuid1())
        data = {
            'data_id' : id_field,
            'data_type' : data_type,
            'value' : value,
            'created_at' : created_at,
            'server_name' : os.environ['SERVER_NAME']
        }
        logging.info(f'Our Generated Data:\n{data}')
        return data


class Send_data():

    def generate_and_send_data(self):
        message = Message()
        generated_data = message.generate_message()

        if generated_data['data_type'] == message.type_list[0]:
            time.sleep(2)
        elif generated_data['data_type'] == message.type_list[-1]:
            time.sleep(4)
        else:
            time.sleep(6)

        queue_send_object = Send_to_Rabbit()
        queue_send_object.connect_to_rabbit()
        queue_send_object.send_message_to_queue(generated_data)


if __name__ == '__main__':
    send_data = Send_data()
    while True:
        send_data.generate_and_send_data()