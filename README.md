# distributed_systems_2023

This project is used for creating a chat application. 

The chat application utilizes publish/subscribe type messaging. The pub/sub messaging is done with Apache Kafka.

Each chat message is saved into a mysql database. 
A separate db_writer.py script handles the database writes by subscribing to the kafka brokers (as a kafka consumer).

Everything except the client runs in a separate Docker container. It is possible to add more kafka-brokers so that higher throughput and reliability is achieved.
By default 2 brokers are up and running. If connection to the other is lost the client will automatically connect to the other one. All the messages are also synchronized between the brokers so it doesn't matter which one is in use.
