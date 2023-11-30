import aiohttp
import asyncio
import pysmartthings
import datetime
import logging
from connections import DatabaseConnection  # Assuming you have a separate file for DatabaseConnection
from security.token_manager import TokenManager
import hashiot
import os
from loggerdb.logger import Logger


class SmartThingsPoller:
    def __init__(self, token_manager, interval_seconds):
        self.token = os.getenv("API_TOKEN")
        self.interval_seconds = interval_seconds
        self.token_manager = token_manager
        self.previous_status_data = {}  # Store the previous status data
        self.logger = Logger()  # Instantiate the Logger class here

        logging.basicConfig(filename="app.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    async def extract(self, device, token):
        async with aiohttp.ClientSession() as session:
            api = pysmartthings.SmartThings(session, token)
            await device.status.refresh()
            status = device.status.values
            dic_status = dict(status)
            cap = device.capabilities
            status_dict = {"capabilities": cap}
            return dic_status

    async def poll_smartthings(self):
        # Establish a database connection
        # Create an instance of the DatabaseConnection class
        db_connector = DatabaseConnection()
        conn = db_connector.get_connection()
        
        try:
            # Validate the API token using the TokenManager instance
            if not self.token_manager.is_valid_token(self.token ):
                logging.error("Unauthorized access: Invalid API token.")
                return

            cursor = conn.cursor()

            while True:
                try:
                    async with aiohttp.ClientSession() as session:
                        api = pysmartthings.SmartThings(session, self.token)
                        devices = await api.devices()

                        for device in devices:
                            status_data = await self.extract(device, self.token)
                            device_id = device.device_id
                            device_name = device.name  # Get the device name
                            current_time = datetime.datetime.now()

                            # Compare current status data with previous data
                            if status_data != self.previous_status_data.get(device_id):
                                self.logger.log_info("Processing device ...........: %s"% device_name)  # Print device name

                                # Create table with device name if it does not exist
                                create_table_query = f"""
                                CREATE TABLE IF NOT EXISTS smartthings_iot (
                                    device_id VARCHAR(255) PRIMARY KEY,
                                    timestamp TIMESTAMP,
                                    device_name TEXT,
                                    data TEXT,
                                    hash TEXT
                                )
                                """

                                cursor.execute(create_table_query)
                                conn.commit()
                                data_hash = hashiot.calculate_hash(str(status_data))

                                create_index_query = f"""
                                CREATE INDEX IF NOT EXISTS idx_smartthings_iot_device_id_timestamp 
                                ON {device_name.replace(" ", "_")} (device_id, timestamp)
                                """
                                cursor.execute(create_index_query)
                                conn.commit()

                                # Insert new record into the device-specific table
                                insert_query = f"INSERT INTO smartthings_iot (device_id, timestamp, device_name, data, hash) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (device_id) DO UPDATE SET data = EXCLUDED.data"
                                cursor.execute(insert_query, (device_id, current_time, device_name.replace(' ', '_'), str(status_data), data_hash))
                                conn.commit()
                                self.logger.log_info("%s Succefully insert" % device_name)



                            # Update previous status data
                            self.previous_status_data[device_id] = status_data

                except Exception as e:
                    self.logger.log_error("Error occurred when while trying to extract data")  # Log errors with context information

                # Sleep for the specified interval before polling again
                await asyncio.sleep(self.interval_seconds)
                self.logger.log_info("SmartThing App Slepping for : %s seconds" % self.interval_seconds) 

        finally:
            # Close the database connection when the loop ends
            if conn is not None:
                db_connector.close_connection()