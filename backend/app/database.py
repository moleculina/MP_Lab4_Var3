# database.py - настройка подключения к базе данных

# Импортируем нужные инструменты из библиотек
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Указываем, где будет храниться файл базы данных
# /data/university.db - это путь внутри контейнера Docker
SQLALCHEMY_DATABASE_URL = "sqlite:////data/university.db"

# Создаём "двигатель" для подключения к БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Эта строчка нужна для SQLite
)

# Создаём фабрику сессий (сессия - это разговор с БД)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаём базовый класс для всех наших таблиц
Base = declarative_base()

# Функция, которая даёт нам доступ к базе данных
def get_db():
    db = SessionLocal()  # Открываем соединение
    try:
        yield db          # Передаём соединение туда, где оно нужно
    finally:
        db.close()        # Закрываем соединение