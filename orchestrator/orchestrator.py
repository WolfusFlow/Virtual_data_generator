import os

from MqItemConsumer import MqItemConsumer

def get_init_data():
    data_dict = os.environ
    return dict(data_dict)

if __name__ == "__main__":
    init_data = get_init_data()
    consume_and_write_object = MqItemConsumer(**init_data)
    consume_and_write_object.connect_consume()
    consume_and_write_object.stop()