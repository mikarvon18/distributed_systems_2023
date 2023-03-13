# distributed_systems_2023

This project is used for creating a chat application. 

The chat application utilizes publish/subscribe type messaging. The pub/sub messaging is done using Apache Kafka.

Each chat message is saved into a mysql database. 
A separate db_writer.py script handles the database writes by subscribing to the kafka brokers (as a kafka consumer).

Everything except the client runs in a separate Docker container. It is possible to add more kafka-brokers so that higher throughput and reliability is achieved.
By default 2 brokers are up and running. If connection to the other is lost the client will automatically connect to the other one. All the messages are also synchronized between the brokers so it doesn't matter which one is in use.

## Using the application

Download the repository to your local pc and extract everything in to the same folder.

After this you should be able to build the docker images and containers by running **'docker compose up -d'**

When you have the containers running, it is possible to use the chatroom with **kafka_ui.py**. Running this program prompts the user to give out a nickname that they can use in the chatroom. After they have given a nickname, they join the chatroom and are able to send messages. Several instances of the UI can be started with different usernames and messages sent from different users are visible in all instances.

When starting the containers, db_writer-1 usually exits and says there are no brokers active. This container can just be started again and it should work just fine.

## Dependencies

The required dependencies for running kafka.ui.py can be installed using pip:
```
pip install kafka-python
pip install tk
pip install mysql-connector-python
```
