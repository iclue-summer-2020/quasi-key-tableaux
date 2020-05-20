FROM python:3.6

COPY . .
RUN python3.6 -m pip install -r requirements.txt
EXPOSE 80
CMD [ "python3.6", "app.py", "--port", "80" ]
