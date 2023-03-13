from tkinter import *
from kafka import KafkaProducer, KafkaConsumer
from threading import Thread
from datetime import datetime
import time
import db_connector
import asyncio


# create Kafka producer and consumer
brokers = ['localhost:9092', 'localhost:9095']
topic = "chat_7"
user_id = None


def set_producer_and_consumer(brokers):
    for broker in brokers:
        try:
            producer = KafkaProducer(bootstrap_servers=broker)
            consumer = KafkaConsumer(topic, bootstrap_servers=broker, auto_offset_reset='earliest')
            print("Broker set: ", broker)
            return consumer, producer
        except:
            continue

    return None




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
def retrieve_old_messages(conn, user_id):
    messages = conn.retrieve_messages(topic)
    for message in messages:
        time_formatted = message[4].strftime("%H:%M:%S")
        if message[1] == user_id:
            user_id_modified = "Me"
        else:
            user_id_modified = message[1]
         

        message_box.insert(END, f'{time_formatted} - {user_id_modified}: {message[2]}\n')

def receive_messages():
    global user_id
    print("whoop")
    global consumer
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

def update_consumer_and_producer():
    global consumer
    global producer
    while True:
        consumer, producer = set_producer_and_consumer(brokers)
        time.sleep(120)


producer = None
consumer = None

consumer, producer = set_producer_and_consumer(brokers)
conn = db_connector.db_connector("localhost", "db", "root", "password")
user_id = input('Enter your user nickname: ')
login_result = conn.login(user_id)
print(login_result)
if login_result == None:
    choice = input("Username not found, would you like to register? (y/n): ")
    print(f"You chose: {choice}")
    if choice == "y":
        if conn.register(user_id) == None:
            print("Username is taken, quitting..")
            quit()
    else:
        print("Quitting... ")
        quit()
else:
    pw = input("Give your password: ")
    if pw != login_result[2]:
        print("Wrong password, quitting app.. ")
        quit()
    




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


retrieve_old_messages(conn, user_id)
conn.close_connection()
# start thread to receive messages


Thread(target=receive_messages).start()
Thread(target=update_consumer_and_producer).start()

# run the Tkinter event loop
window.mainloop()