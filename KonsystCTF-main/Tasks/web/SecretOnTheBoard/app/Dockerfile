FROM python:3.9-slim

WORKDIR /app

ENV ENCRYPTED_FLAG="Z21iaHx4aTFgbTRndWB1aTIlYGk0c2ZAfiUl" 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]