import os
import hashlib
import os
from dotenv import load_dotenv
from connections import DatabaseConnection
import logging
from loggerdb.logger import Logger


# Load environment variables from .env file
load_dotenv()



class UserCredentialProvider:


    def __init__(self):
        self.USER_USERNAME = os.getenv("USER_USERNAME")
        self.USER_PASSWORD= os.getenv("USER_PASSWORD")
        self.db_connector = DatabaseConnection()
        self.logger = Logger()

    def validate_user_credentials(self):
        # Fetch hashed password from secure storage (database, config file, etc.)
        stored_password = self.get_stored_password(self.USER_USERNAME)

        # Hash the provided password for comparison
        hashed_password = hashlib.sha256(self.USER_PASSWORD.encode()).hexdigest()

        # Compare the hashed passwords
        if hashed_password == stored_password:
            self.logger.log_info("Successfully authenticated the user: %s" % self.USER_USERNAME)

            return True
        self.logger.log_info("Failed to authenticated the user: %s" % self.USER_USERNAME)
        return False


    def get_stored_password(self, username):
        try:
            conn = self.db_connector.get_connection()
            cursor = conn.cursor()

            # Use a tuple to pass the username as a parameter to avoid SQL injection
            cursor.execute("SELECT password_hash FROM users_smartthings WHERE username = %s;", (username,))
            stored_password = cursor.fetchone()

            # If the user is found, return the stored password hash, otherwise return None
            return stored_password[0] if stored_password else None

        except Exception as e:
            self.logger.log_error("Failed to authenticate the user: %s" % username)
            # Handle the exception (log it, raise it, etc.) based on your application's needs
            raise

        finally:
            # Close the cursor and connection in the finally block to ensure they are always closed
            cursor.close()
            conn.close()
    



