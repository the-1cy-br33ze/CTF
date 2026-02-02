FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y openssl && \
    pip install flask cryptography
RUN touch /app/users.db
CMD ["python", "app.py"]