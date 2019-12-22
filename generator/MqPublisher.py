import os
import pika
import json
import logging

logging.basicConfig(filename=f"mqpublisher_{os.environ['SERVER_NAME']}_log_file",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

class MqPublisher():

    def __init__(self, *args, **kwargs):
        try:
            self.ampq_url    = kwargs['AMQP_URL']
            self.routing_key = kwargs['ROUTING_KEY']
        except KeyError as ke:
            logging.exception(f'Exception in MqItemComsumer Initialization:\n {ke}')

    mq_connection = None
    mq_channel = None
    

    def connect_to_rabbit(self):
        try:
            self.mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.ampq_url))

        except pika.exceptions.AMQPConnectionError as error:
            logging.exception(f'Error in AMQP connection: {error}')

        if self.mq_connection.is_open:
            self.mq_channel = self.mq_connection.channel()
            self.mq_channel.queue_declare(queue=self.routing_key, durable=True)


    def send_message_to_queue(self, message):
        try:
            self.mq_channel.basic_publish(exchange='',
                                          routing_key=self.routing_key,
                                          body=json.dumps(message),)
        
        except pika.exceptions.ChannelError as error:
            logging.exception(f'error with channel on message send: {error}')

    def close(self):
        self.mq_connection.close()
