FROM python:3.9
COPY . /app
WORKDIR /app
# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

ENTRYPOINT FLASK_APP=app flask run --host=0.0.0.0
EXPOSE 5000