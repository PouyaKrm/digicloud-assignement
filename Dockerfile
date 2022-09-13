FROM python:3.9.13-slim
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
