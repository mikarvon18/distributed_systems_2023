from tkinter import *
from kafka import KafkaProducer, KafkaConsumer
from threading import Thread
from datetime import datetime
import db_connector

# create Kafka producer and consumer
topic = "chat_7"
user_id = input('Enter your user ID: ')
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest')




# function to send message to Kafka topic
def send_message():
    now = datetime.now()
    time_formatted = now.strftime("%H:%M:%S")
    print(user_id)
    print("Sends a message!")
    message = input_box.get()
    full_message = f'{time_formatted};{user_id};{message}'
    producer.send(topic, full_message.encode())
    input_box.delete(0, END)

# function to receive messages from Kafka topic
def retrieve_old_messages(conn):
    global user_id
    messages = conn.retrieve_messages(topic)
    for message in messages:
        time_formatted = message[4].strftime("%H:%M:%S")
        if message[1] == user_id:
            user_id_modified = "me"
        else:
            user_id_modified = message[1]
         

        message_box.insert(END, f'{time_formatted} - {user_id_modified}: {message[2]}\n')

def receive_messages():
    print("whoop")
    global user_id
    # get all messages sent to the topic since the beginning
    """
    all_messages = consumer.poll(timeout_ms=1000)
    for messages in all_messages.values():
        for message in messages:
            decoded_message = message.value.decode()
            time_formatted, user_id_from_message, message_text = decoded_message.split(';', 2)
            if user_id_from_message == user_id:
                user_id_modified = "Me"
            else:
                user_id_modified = user_id_from_message

            message_box.insert(END, f'{time_formatted} - {user_id_modified}: {message_text}\n')
    """
    # start receiving new messages
    for message in consumer:
        print("reading...")
        decoded_message = message.value.decode()
        time_formatted, user_id_from_message, message_text = decoded_message.split(';', 2)
        if user_id_from_message == user_id:
            user_id_modified = "Me"
        else:
            user_id_modified = user_id_from_message

        message_box.insert(END, f'{time_formatted} - {user_id_modified}: {message_text}\n')



# create Tkinter window
window = Tk()
window.title(f'Chat App - {user_id}')

# create input box and send button
input_box = Entry(window, width=50)
input_box.pack(side=LEFT, padx=5, pady=5)
send_button = Button(window, text='Send', command=send_message)
send_button.pack(side=LEFT, padx=5, pady=5)

# create message box
message_box = Text(window, width=50)
message_box.pack(side=LEFT, padx=5, pady=5)

conn = db_connector.db_connector("localhost", "db", "root", "password")
retrieve_old_messages(conn)
conn.close_connection()
# start thread to receive messages
Thread(target=receive_messages).start()

# run the Tkinter event loop
window.mainloop()