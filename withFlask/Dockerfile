<<<<<<< HEAD
FROM python:3.11-alpine
WORKDIR . .
COPY menu.py .
CMD [ "python menu.py" ]
=======
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
CMD [ "python3","app.py" ]
>>>>>>> 5bb46dd8fad19a28c6f6485f15fab0696870ccb6
