# syntax=docker/dockerfile:1

FROM python:3.10
WORKDIR /app
RUN pwd
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .


#CMD [ "python3", "-m" , "db_writer.py"]
