import db_connector
from threading import Thread
from kafka import KafkaProducer, KafkaConsumer

print("Hello world")

topic = "chat_7"
consumer = KafkaConsumer(topic, bootstrap_servers=['broker:9093'])

def receive_messages(conn):
    while True:
        for message in consumer:
            decoded_message = message.value.decode()
            time_formatted, user_id_from_message, message_text = decoded_message.split(';', 2)

            print(f'{time_formatted} - {user_id_from_message}: {message_text}\n')
            conn.insert_message(user_id_from_message, message_text, topic)
def main():
    print("Hello World!")
    conn = db_connector.db_connector("distributed_systems-mysql_db-1", "db", "root", "password")
    conn.retrieve_users()
    receive_messages(conn)
    #Thread(target=receive_messages(conn)).start()
    

if __name__=='__main__':
    main()