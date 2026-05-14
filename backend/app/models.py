# models.py - описываем структуру таблиц базы данных

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# ТАБЛИЦА "СТУДЕНТЫ"
class Student(Base):
    __tablename__ = "students"  # Имя таблицы в базе данных

    # Описываем колонки (столбцы) таблицы
    id = Column(Integer, primary_key=True, index=True)  # Уникальный номер студента
    name = Column(String, index=True)  # Имя студента
    group = Column(String)  # Группа студента

    # Связь с таблицей оценок (один студент может иметь много оценок)
    grades = relationship("Grade", back_populates="student")


# ТАБЛИЦА "ДИСЦИПЛИНЫ"
class Discipline(Base):
    __tablename__ = "disciplines"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный номер дисциплины
    name = Column(String, unique=True, index=True)  # Название предмета
    credits = Column(Integer)  # Количество кредитов

    # Связь с таблицей оценок
    grades = relationship("Grade", back_populates="discipline")


# ТАБЛИЦА "ОЦЕНКИ"
class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)  # Уникальный номер оценки
    student_id = Column(Integer, ForeignKey("students.id"))  # Какой студент получил
    discipline_id = Column(Integer, ForeignKey("disciplines.id"))  # По какому предмету
    score = Column(Float)  # Оценка (2, 3, 4, 5)

    # Связи с другими таблицами
    student = relationship("Student", back_populates="grades")
    discipline = relationship("Discipline", back_populates="grades")