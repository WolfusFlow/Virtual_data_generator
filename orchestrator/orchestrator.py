import os
import pika
import psycopg2

AMPQ_URL    = os.environ['AMQP_URL']
ROUTING_KEY = os.environ['ROUTING_KEY']
POSTGRESQL  = os.environ['POSTGRESQL']
DATABASE    = os.environ['DATABASE']
DB_USER     = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']


def main():
    try:
        mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMPQ_URL))
        channel = mq_connection.channel()
        channel.queue_declare(queue=ROUTING_KEY)

        def callback(ch, method, properties, body):
            print(f'Received message: {body}')
            work_with_data(body)

        channel.basic_consume(queue=ROUTING_KEY,
                              auto_ack=True,
                              on_message_callback=callback)
        channel.start_consuming()

    except (Exception, pika.exceptions.AMQPConnectionError) as error:
        print(f'error in mq orchestrator connection: {error}') 


def work_with_data(data):
    #ckeck our data cut this later
    print(data)
    try:
        db_connection = psycopg2.connect(host     = POSTGRESQL,
                                         database = DATABASE, 
                                         user     = DB_USER, 
                                         password = DB_PASSWORD)
        cursor = db_connection.cursor()
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        #check connection cut this later
        print('postgres_version:::::\n\n')
        print(f'{db_version}\n\n')
        #Write_to_database
        # check_exist_table = 
        create_table_query = '''CREATE TABLE virtual_data_table
          (ID INT PRIMARY KEY     NOT NULL,
          SERVER_NAME     TEXT    NOT NULL,
          DATA_TYPE       TEXT    NOT NULL,
          VALUE           TEXT    NOT NULL,
          CREATED_AT      TIMESTAMP); '''
        # cursor.execute(create_table_query)
        # db_connection.commit()

        insert_data_into_table = f'''INSERT INTO virtual_data_table
          (SERVER_NAME, DATA_TYPE, VALUE, CREATED_AT) VALUES
          ({data.server_name}, {data.data_type}, {data.value}, {data.created_at})'''
        # cursor.execute(insert_data_into_table)
        # db_connection.commit()

        #Del_old_data_from_it
                                        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'error in database orchestrator: {error}')


if __name__ == "__main__":
    main()