# Base python image
FROM python:3.8.12

# Set working dir
WORKDIR /mnist_service

# Copy requirements.txt to docker container
COPY ./requirements.txt /mnist_service/requirements.txt

# Install packages from requirements.txt on docker container
RUN pip install -r requirements.txt

# Add app file
COPY . /mnist_service
ENV FLASK_APP=app

EXPOSE 8000

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
