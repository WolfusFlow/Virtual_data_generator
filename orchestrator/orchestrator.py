import os
import pika
import json
import datetime as dt
import psycopg2

AMPQ_URL    = os.environ['AMQP_URL']
ROUTING_KEY = os.environ['ROUTING_KEY']
POSTGRESQL  = os.environ['POSTGRESQL']
DATABASE    = os.environ['DATABASE']
DB_USER     = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
TABLE_NAME  = os.environ['TABLE_NAME']

life_time   = str(dt.datetime.now()-dt.timedelta(days=1)).split('.')[0]


def main():
    try:
        mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host=AMPQ_URL))
        channel = mq_connection.channel()
        channel.queue_declare(queue=ROUTING_KEY)

        def callback(ch, method, properties, body):
            work_with_data(json.loads(body.decode('UTF-8')))

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
        
        #Check if table exist
        cursor.execute(f"select exists(select relname from pg_class where relname='{TABLE_NAME}')")
        exists = cursor.fetchone()[0]
        if not exists:
            create_table_query = f'''CREATE TABLE {TABLE_NAME}
              (ID INT GENERATED ALWAYS AS IDENTITY,
              UUID            TEXT    NOT NULL,
              SERVER_NAME     TEXT    NOT NULL,
              DATA_TYPE       TEXT    NOT NULL,
              VALUE           INT     NOT NULL,
              CREATED_AT      TEXT    NOT NULL); '''
            cursor.execute(create_table_query)
            db_connection.commit()

        #Del_old_data_from_database
        def delete_data_from_database(db_connection, cursor):
            try:
                delete_data_from_table = f'''DELETE FROM {TABLE_NAME}
                WHERE CREATED_AT <= '{life_time}'
                '''
                #WHERE >= TIMESTAMP 'yesterday' hmm should I do it through a query?
                cursor.execute(delete_data_from_table)
                db_connection.commit()

            except Exception as e:
                print(f'error on delete from database: {e}')


        def insert_data_into_database(db_connection, cursor):
            try:
                insert_data_into_table = f'''INSERT INTO {TABLE_NAME}
                  (UUID, SERVER_NAME, DATA_TYPE, VALUE, CREATED_AT) VALUES
                  ('{data['data_id']}', '{data["server_name"]}', '{data["data_type"]}', '{data["value"]}', '{data["created_at"]}')'''
            #wanna see the output  cut this later
                print('this is inserting')
                print(insert_data_into_table)
                cursor.execute(insert_data_into_table)
                db_connection.commit()

            except Exception as e:
                print(f'error on insert to database: {e}')


        
        insert_data_into_database(db_connection, cursor)
        delete_data_from_database(db_connection, cursor)
        cursor.close()
        db_connection.close()

                                        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'error in database orchestrator: {error}')


if __name__ == "__main__":
    main()