FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port on which the Uvicorn server will run
EXPOSE 8000

# Set the environment variable for Uvicorn
ENV MODULE_NAME=app
ENV VARIABLE_NAME=app

# Run the Uvicorn server
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app:app"]