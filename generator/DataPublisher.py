import os
import uuid
import random
import logging
import datetime as dt

from MessageType import MessageType
from MqPublisher import MqPublisher

logging.basicConfig(filename=f"data_publisher_{os.environ['SERVER_NAME']}_log_file",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

class DataPublisher():
    publisher= None

    def __init__(self, *args, **kwargs):
        self.publisher = MqPublisher(**kwargs)
        self.publisher.connect_to_rabbit()


    def generate_message(self):
        created_at = str(dt.datetime.now()).split('.')[0]
        data_type = random.choice(list(MessageType)).value
        print(data_type)
        value = random.randrange(0, 12000, 125)
        id_field = str(uuid.uuid1())
        data = {
            'data_id' : id_field,
            'data_type' : data_type,
            'value' : value,
            'created_at' : created_at,
            'server_name' : os.environ['SERVER_NAME']
        }
        return data

    def publish_data(self, message):
        if self.publisher.mq_connection.is_open:
            logging.info(f'Sending Message: {message}')
            self.publisher.send_message_to_queue(message)
        else:
            logging.error('Publisher connection closed!!! ')
            return None

    def close(self):
        self.publisher.close()

