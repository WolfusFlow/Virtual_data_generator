import time

from MqItemConsumer import MqItemConsumer

if __name__ == "__main__":
    consume_and_write_object = MqItemConsumer()
    while True:
        consume_and_write_object.connect_consume()
        time.sleep(1)
    
    consume_and_write_object.stop()