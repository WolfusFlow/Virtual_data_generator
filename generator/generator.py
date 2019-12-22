import time
import os

from  DataPublisher import DataPublisher
from  MessageType import MessageType

def get_init_data():
    data_dict = os.environ
    return dict(data_dict)

if __name__ == '__main__':
    init_data = get_init_data()
    publisher = DataPublisher(**init_data)
    while True:
        generated_message = publisher.generate_message()

        if generated_message['data_type'] is MessageType.Type_A:
            time.sleep(2)
        elif generated_message['data_type'] is MessageType.Type_C:
            time.sleep(4)
        else:
            time.sleep(6)

        publisher.publish_data(generated_message)

    publisher.close()