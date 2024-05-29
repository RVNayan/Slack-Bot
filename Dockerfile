####
### To build the Image - docker build -t slack-bot-app .
### To run the image - docker run -p 4040:4040 -p 5000:5000 --env-file .env slack-bot-app

### Handling the image
### 1. docker save -o <path for generated tar file> <image name>
### 2. docker load -i <path to image tar file>

####
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    unzip \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list \
    && apt-get update \
    && apt-get install -y ngrok

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=botauto.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 to allow communication to/from the container
EXPOSE 5000

# Authenticate ngrok
RUN ngrok config add-authtoken 2gtxStCwdAXjzK4AeYOjQZWEAVq_5QpGowEawgZQcp2whpS6M

# Start ngrok and Flask app together (imp)
CMD ngrok http 5000 --domain=friendly-helped-hamster.ngrok-free.app & python3 -u -m flask run --host=0.0.0.0 --port=5000
