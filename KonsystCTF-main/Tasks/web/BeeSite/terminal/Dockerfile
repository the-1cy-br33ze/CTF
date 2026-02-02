FROM python:3.11-alpine

# Установка зависимостей
RUN pip install flask flask_cors

# Создание рабочей папки
WORKDIR /app

# Копируем код и флаг
COPY app.py .
COPY flag.txt .

# Открываем порт
EXPOSE 5000

# Запуск
CMD ["python", "app.py"]
