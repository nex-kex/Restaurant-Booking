# Указываем базовый образ
FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /materials

# Копируем файлы для Poetry
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]