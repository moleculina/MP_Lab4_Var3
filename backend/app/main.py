# main.py - главный файл, который запускает сервер

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models, routes

# СОЗДАЁМ ТАБЛИЦЫ В БАЗЕ ДАННЫХ
# Проверяем, есть ли уже таблицы, если нет - создаём
Base.metadata.create_all(bind=engine)


def seed_data():
    """
    ЗАПОЛНЯЕМ БАЗУ ДАННЫХ ТЕСТОВЫМИ ДАННЫМИ
    Это выполнится только при первом запуске
    """
    from sqlalchemy.orm import Session
    from .database import SessionLocal

    db = SessionLocal()

    # Проверяем, есть ли уже студенты в базе
    if db.query(models.Student).count() == 0:
        print("Добавляем тестовые данные...")

        # Добавляем студентов
        students = [
            models.Student(name="Иванов Иван", group="ИС-21"),
            models.Student(name="Петрова Анна", group="ИС-21"),
            models.Student(name="Сидоров Сергей", group="ИС-22"),
            models.Student(name="Козлова Елена", group="ИС-22"),
        ]
        db.add_all(students)
        db.commit()

        # Добавляем дисциплины
        disciplines = [
            models.Discipline(name="Базы данных", credits=4),
            models.Discipline(name="Программирование", credits=5),
            models.Discipline(name="Математика", credits=4),
        ]
        db.add_all(disciplines)
        db.commit()

        # Добавляем оценки
        # student_id=1 это Иванов, discipline_id=1 это Базы данных, score=5
        grades = [
            models.Grade(student_id=1, discipline_id=1, score=5.0),
            models.Grade(student_id=1, discipline_id=2, score=4.5),
            models.Grade(student_id=1, discipline_id=3, score=4.0),
            models.Grade(student_id=2, discipline_id=1, score=4.5),
            models.Grade(student_id=2, discipline_id=2, score=5.0),
            models.Grade(student_id=2, discipline_id=3, score=4.5),
            models.Grade(student_id=3, discipline_id=1, score=3.5),
            models.Grade(student_id=3, discipline_id=2, score=3.0),
            models.Grade(student_id=4, discipline_id=1, score=5.0),
            models.Grade(student_id=4, discipline_id=2, score=5.0),
            models.Grade(student_id=4, discipline_id=3, score=4.5),
        ]
        db.add_all(grades)
        db.commit()
        print("Тестовые данные добавлены!")

    db.close()


# СОЗДАЁМ ПРИЛОЖЕНИЕ FASTAPI
app = FastAPI(title="University Portal API")

# НАСТРАИВАЕМ CORS (разрешаем сайту обращаться к серверу)
# Без этого браузер заблокирует запросы
origins = [
    "http://localhost:5500",  # локальный запуск фронтенда
    "http://localhost:8080",  # запуск фронтенда в Docker
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8080",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # разрешаем все HTTP методы
    allow_headers=["*"],  # разрешаем все заголовки
)

# ПОДКЛЮЧАЕМ НАШИ МАРШРУТЫ
app.include_router(routes.router)


# ЗАПУСКАЕМ ДОБАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ ПРИ СТАРТЕ
@app.on_event("startup")
def on_startup():
    seed_data()


# КОРНЕВОЙ АДРЕС (проверка, что сервер работает)
@app.get("/")
def root():
    return {"message": "University Portal API is running"}