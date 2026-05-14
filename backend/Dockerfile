FROM python:3.11-slim

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем requirements.txt (он в корне проекта, НЕ в папке backend!)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЁ содержимое текущей папки (где лежит Dockerfile)
# В контексте сборки "текущая папка" — это папка backend
COPY ./backend /project/backend

EXPOSE 8010

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8010"]