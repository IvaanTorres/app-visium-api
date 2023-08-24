# Use the official Python image as the base image
FROM python:3.9-slim as dev

# Set environment variables to ensure Python output is unbuffered
ENV PYTHONUNBUFFERED 1

# Install Pipenv globally
RUN pip install pipenv

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock into the container
COPY pipfile pipfile.lock /app/

# Install project dependencies using Pipenv
# RUN pipenv shell
RUN pipenv install
RUN pip install fastapi
RUN pip install uvicorn

# Copy the local code into the container
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
# CMD ["pipenv", "run", "uvicorn", "app.main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]
CMD ["pipenv", "run", "start"]
