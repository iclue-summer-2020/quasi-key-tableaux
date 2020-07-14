FROM python:3.6-slim

COPY . .
RUN python3.6 -m pip install -r requirements.txt
EXPOSE 5000
CMD exec gunicorn --bind :5000 --workers 1  --threads 8 --timeout 0 app:app
