import psycopg2
import logging
import os
from dotenv import load_dotenv
from loggerdb.logger import Logger


class DatabaseConnection:
    def __init__(self):
        # Set up Logstash handler
        # logstash_handler = TCPLogstashHandler("localhost", 9200, version=1)
        # logger = logging.getLogger('your_logger_name')  # Replace 'your_logger_name' with an appropriate logger name
        # logger.setLevel(logging.INFO)  # Set the desired logging level
        # logger.addHandler(logstash_handler)
        load_dotenv()
        self.logger = Logger()  # Instantiate the Logger class here


        # Access environment variables
        db_user = os.getenv("DB_USER")



        try:
            self.conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
        )
        except psycopg2.OperationalError as e:
            self.logger.log_error({"Error occurred while establishing database connection by user": db_user, "error": str(e)})
            raise


    def get_connection(self):
        return self.conn

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
