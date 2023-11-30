import logging
import psycopg2

class Logger:
    def __init__(self):
        # Configure logging settings
        logging.basicConfig(filename="logs/app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


        # Create a custom logging handler for database logging
        self.db_handler = self.DatabaseHandler()
        self.db_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(self.db_handler)

    class DatabaseHandler(logging.Handler):
        def __init__(self):
            super().__init__()
            self.conn = psycopg2.connect(
                database="postgres",
                user="postgres",
                password="postgres",
                host="localhost",
                port="5432"
            )
            self.create_log_table()

        def create_log_table(self):
            with self.conn.cursor() as cursor:
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS logs 
                               (id SERIAL PRIMARY KEY, 
                               timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                               level TEXT, 
                               message TEXT)
                               ''')
            self.conn.commit()

        def emit(self, record):
            log_entry = (record.levelname, self.format(record))
            self.insert_log_entry(log_entry)

        def insert_log_entry(self, log_entry):
            with self.conn.cursor() as cursor:
                cursor.execute("INSERT INTO logs (level, message) VALUES (%s, %s)", log_entry)
            self.conn.commit()

        def close_connection(self):
            self.conn.close()

    def log_info(self, message):
        logging.info(message)

    def log_error(self, message):
        logging.error(message)

    def __del__(self):
        # Close the database connection when the Logger instance is deleted
        self.db_handler.close_connection()


