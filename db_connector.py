import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time

mySql_Create_Users_Query = """CREATE TABLE if not exists Users ( 
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    Name varchar(250) NOT NULL,
                                    Password varchar(250) NOT NULL)"""

mySql_Create_Messages_Query = """CREATE TABLE if not exists Messages ( 
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    Sender varchar(250) NOT NULL,
                                    Message varchar(250),
                                    Topic varchar(250) NOT NULL,
                                    time_sent timestamp NOT NULL)"""

class user(object):
    def __init__(self, id, username):
        self.id = id
        self.username = username

class db_connector(object):
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = self.create_connection()
        

    def create_connection(self):
        connection = None
        try:
            connection = mysql.connector.connect(host=self.host,
                                                database=self.database,
                                                user=self.user,
                                                password=self.password)
            if connection.is_connected():
                return connection
                

        except Error as e:
            print("Error while connecting to MySQL", e)

    def retrieve_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users")
        result = cursor.fetchall()
        for user in result:
            print(f"ID: {user[0]}, Nick: {user[1]}")
    
    def commit(self):
        self.connection.commit()

    def register(self, nickname):
        user_name = nickname
        password = input("Password: ")
        sql = "INSERT INTO Users (Name, Password) VALUES (%s, %s)"
        cursor = self.connection.cursor()
        val = (user_name, password)
        cursor.execute(sql, val)
        self.commit()
        print(cursor.rowcount, "was inserted.")
    
    def login(self, nickname=0):
        if nickname == 0:
            nickname = input("Login as: ")

        cursor = self.connection.cursor()
        sql = f"SELECT * FROM Users WHERE Name='{nickname}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    
    def insert_message(self, sender, message, topic):
        ts = time.time()
        now = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(now)
        sql = "INSERT INTO Messages (Sender, Message, Topic, time_sent) VALUES (%s, %s, %s, %s)"
        cursor = self.connection.cursor()
        val = (sender, message, topic, now)
        cursor.execute(sql, val)
        self.commit()
        print("New message inserted")

    def create_table(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.commit()
    
    def drop_table(self, table):
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE {table}")
        self.commit()

    def retrieve_messages(self, topic):
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM Messages WHERE Topic='{topic}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    def show_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("show tables;")
        results = cursor.fetchall()

        return results
    def close_connection(self):
        self.connection.close()

def main():
    db_con = db_connector("localhost", "db", "root", "password")
    db_con.drop_table("Messages")
    db_con.create_table(mySql_Create_Messages_Query)
    db_con.create_table(mySql_Create_Users_Query)
    db_con.retrieve_users()
    
    
    #db_con.register()
    nickname = "test2"
    login_result = db_con.login(nickname)
    print(login_result)
    if login_result == None:
        db_con.register(nickname)

    messages = db_con.retrieve_messages("chat_7")
    for message in messages:
        print(message)
    
    print(db_con.show_tables())
    db_con.close_connection()


if __name__ == '__main__':
    main()