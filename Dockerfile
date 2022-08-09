FROM python:3.9
# Устанавливаем переменную среды (хз зачем)
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
# Устанавливаем зависимости
RUN pip install -r requirements.txt