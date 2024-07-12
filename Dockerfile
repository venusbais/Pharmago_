# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /webapp

# Copy the requirements.txt file into the container at /app
COPY req.txt .

# Install any dependencies specified in requirements.txt
RUN pip install -r req.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app
CMD ["flask", "run"]