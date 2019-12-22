import os
import unittest
import pika

from generator import Message, Send_to_Rabbit

class TestGenerator(unittest.TestCase):
    pass

#TODO: Write Tests on Generator

#     def test_generate_message(self):
#         message = Message()
#         data = message.generate_message()
#         self.assertEqual(data['server_name'], os.environ['SERVER_NAME'])
#         self.assertEqual(data['data_type'] in message.type_list, True)

#     def test_rabbit_consume_message_from_the_queue(self):

#         message = 'testMessage'
#         routing_key = 'test_queue'

#         rabbit = Send_to_Rabbit()
#         rabbit.routing_key = routing_key

#         rabbit.connect_to_rabbit()

#         self.assertEqual(rabbit.mq_connection.is_open, True)
        
#         rabbit.mq_channel.basic_publish(exchange='',
#                             routing_key=routing_key,
#                             body=message)

#         queue = rabbit.mq_channel.queue_declare(
#             queue=routing_key, durable=True,
#             exclusive=False, auto_delete=False)
#         assert queue.method.message_count >= 1

#         rabbit.send_message_to_queue(message)

#         consumer = Test_Consumer(routing_key)

#         consumer.connect_consume()

#         queue_consumer = consumer.mq_channel.queue_declare(
#             queue=routing_key, durable=True,
#             exclusive=False, auto_delete=False)

#         self.assertEqual(queue_consumer.method.message_count, 0)

#         consumer.mq_channel.stop_consuming()


# class Test_Consumer():
#     def __init__(self, routing_key):
#         self.rabbit = os.environ['AMQP_URL']
#         self.routing_key = routing_key

#     mq_connection = None
#     mq_channel    = None

#     def connect_consume(self):
#         self.mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbit))
#         self.mq_channel = self.mq_connection.channel()
#         self.mq_channel.queue_declare(queue=self.routing_key, durable=True)
#         self.mq_channel.basic_consume(queue=self.routing_key,
#                                       on_message_callback=self.callback,
#                                       auto_ack=True,)


#     def callback(self):
#         pass


if __name__ == '__main__':
    unittest.main()