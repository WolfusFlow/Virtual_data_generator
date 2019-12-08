import os
import json
import time
import datetime as dt
import logging

import pika
import psycopg2

from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

from database import Session, engine, Base
from db_model import VirtualData

logging.basicConfig(filename="orchestrator_log_file",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s \n\n',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


class Rabbit_connection():

    def __init__(self):
        self.amqp_url    = os.environ['AMQP_URL']
        self.routing_key = os.environ['ROUTING_KEY']
        self.db_session  = Session() 

    mq_connection = None
    mq_channel    = None


    def callback(self, channel, method, properties, body):

        decoded_body = json.loads(body.decode('UTF-8'))

        insert_to_database = VirtualData(decoded_body['data_id'], decoded_body['server_name'], 
        decoded_body['data_type'], decoded_body['value'], decoded_body['created_at'])

        logging.info(f'inserted data:::::::::\n {insert_to_database}')
        self.db_session.add(insert_to_database)
        self.db_session.commit()


    def connect_consume(self):
        try:
            self.mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.amqp_url))
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
            self.db_session.close()
        
        except pika.exceptions.AMQPConnectionError as error:
            print(f'error in connection::::: {error}')


class Write_data_to_database():

    def consume_from_queue_and_writedown(self):
        logging.info('let\'s go')
        mq_connection = Rabbit_connection()
        mq_connection.connect_consume()


if __name__ == "__main__":
    consume_and_write_object = Write_data_to_database()
    while True:
        consume_and_write_object.consume_from_queue_and_writedown()
        time.sleep(1)