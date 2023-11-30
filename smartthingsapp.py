import aiohttp
import asyncio
import psycopg2
import pysmartthings
import hashlib
from connections import DatabaseConnection
import datetime
import logging
import hashiot
from security.token_manager import TokenManager
from security.usercredentials import UserCredentialProvider
from smartthingspoller import SmartThingsPoller
import os
import sys


def main():
    # Initialize the TokenManager

    token_manager = TokenManager()
    user_credentials_prodiver = UserCredentialProvider()
    if(user_credentials_prodiver.validate_user_credentials() == True):
        polling_interval_seconds = 10
        smartthingspoller = SmartThingsPoller(token_manager, polling_interval_seconds)
        asyncio.run(smartthingspoller.poll_smartthings())



    

if __name__ == "__main__":
    main()