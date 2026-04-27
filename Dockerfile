FROM python:3.12.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

Copy . .

CMD ["gunicorn", "taskApi.wsgi", "--bind", "0.0.0.0:8000"]