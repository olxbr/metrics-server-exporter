FROM python:3.6-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
CMD ["python", "app.py"]
