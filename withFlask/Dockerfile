FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app-flask.py .
EXPOSE 8080/udp
CMD [ "python3","app-flask.py" ]

