# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory into the container at /app
COPY . /app

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Redirect Python logs to a local log file
RUN mkdir -p /app/logs
RUN touch /app/logs/app.log

# Run your Python script and redirect logs to the local log file
CMD ["sh", "-c", "python -u smartthingsapp.py 2>&1 | tee -a /app/logs/app.log"]
