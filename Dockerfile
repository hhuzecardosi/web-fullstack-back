FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN python3 initiate.py
CMD ["python3", "main.py"]
EXPOSE 5100