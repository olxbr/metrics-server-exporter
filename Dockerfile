FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip install --requirement requirements.txt

COPY . /app
CMD ["python", "app.py"]
