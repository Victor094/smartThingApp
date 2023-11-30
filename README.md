# **SmartThings Data Logger with Postgres**

This application is designed to read data from SmartThings, log any errors encountered during the process, and securely save IoT device data to a PostgreSQL database after hashing it for enhanced security.

## Installation

Please follow the steps below to install and run the application:

1. Clone this repository using the following command:
```
git clone
```

2. Install the required dependencies by running:
```
sudo docker build --no-cache -t smartthingsapp .

```

3. Create a `.env` file in the root directory of the project and add the necessary configuration variables as shown in the section below.

4. Start the application by running:
```
docker run -v :/app/log --network host smartthingsapp

```

## Configuration

To configure the application, create a `.env` file in the root directory with the following variables:


- `DATABASE_URL`: The connection URL for your PostgreSQL database.
- `SMARTTHINGS_API_KEY`: The API key obtained from SmartThings.

Make sure to replace ``, ``, ``, ``, ``, ``, and `` with your specific values.

## Usage

Once you have successfully installed and configured the application, it will automatically start reading data from SmartThings devices and saving it securely into your PostgreSQL database.

The application logs any errors encountered during this process, which can be found in the console output or logged into a separate log file depending on your preferred logging setup.

