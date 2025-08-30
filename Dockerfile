FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Pillow dependencies
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libtiff-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Define the command to run the application（用Shell格式，确保$PORT扩展）
CMD gunicorn app:app --bind 0.0.0.0:$PORT