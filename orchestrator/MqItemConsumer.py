import os
import json
import datetime as dt
import logging

import pika
import psycopg2

from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

from database import DataBaseConnection

logging.basicConfig(filename=__name__,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s \n\n',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class MqItemConsumer():

    def __init__(self):
        self.amqp_url      = os.environ['AMQP_URL']
        self.routing_key   = os.environ['ROUTING_KEY']
        self.db_connection = DataBaseConnection()
        self.db_connection.connect()

    mq_connection = None
    mq_channel    = None


    def callback(self, channel, method, properties, body):
        decoded_body = json.loads(body.decode('UTF-8'))
        logging.info(f'inserted data:::::::::\n {decoded_body}')
        self.db_connection.write_to_database(decoded_body)


    def connect_consume(self):
        try:
            self.mq_connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.amqp_url))
        except pika.exceptions.AMQPConnectionError as error:
            logging.exception(f'error in connection::::: {error}')
        
        if self.mq_connection.is_open:
                self.mq_channel = self.mq_connection.channel()
                self.mq_channel.queue_declare(queue=self.routing_key, durable=True)
                self.mq_channel.basic_consume(queue=self.routing_key,
                                              on_message_callback=self.callback,
                                              auto_ack=True,)
                try:
                    self.mq_channel.start_consuming()

                except KeyboardInterrupt:
                    self.mq_channel.stop_consuming()

        self.mq_channel.close()
        self.db_connection.close()

    def stop(self):
        self.mq_channel.close()
        self.mq_connection.close()
        self.db_connection.close()
