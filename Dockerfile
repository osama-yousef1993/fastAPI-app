# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY ./app /code/app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable for the database URL
ENV DATABASE_URL="postgresql://user:password@postgres/dbname"

# Run the app. CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]