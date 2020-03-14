FROM python:3.7

WORKDIR /app

COPY . .

COPY main.py /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt