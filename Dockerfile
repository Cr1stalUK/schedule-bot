# Базовый образ
FROM python:3.11-slim

# Создаём рабочую папку приложения
WORKDIR /app

# Сначала устанавливаем необходимые библиотеки
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Копируем основные файлы бота
COPY ./bot.py *.json /app/

# Команда запуска бота
CMD [ "python", "bot.py" ]
