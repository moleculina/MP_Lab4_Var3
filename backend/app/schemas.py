# schemas.py - описываем формат данных для передачи

from pydantic import BaseModel
from typing import List, Optional


# ----- СХЕМЫ ДЛЯ СТУДЕНТОВ -----
class StudentBase(BaseModel):
    """Базовые поля студента"""
    name: str  # имя
    group: str  # группа


class StudentCreate(StudentBase):
    """Для создания нового студента"""
    pass  # ничего не добавляем, просто наследуем


class StudentOut(StudentBase):
    """Для выдачи информации о студенте"""
    id: int  # ID студента
    average_score: Optional[float] = None  # средний балл (может быть пустым)

    class Config:
        from_attributes = True  # разрешаем работать с SQLAlchemy моделями


# ----- СХЕМЫ ДЛЯ ДИСЦИПЛИН -----
class DisciplineBase(BaseModel):
    name: str  # название
    credits: int  # кредиты


class DisciplineCreate(DisciplineBase):
    pass


class DisciplineOut(DisciplineBase):
    id: int

    class Config:
        from_attributes = True


# ----- СХЕМЫ ДЛЯ ОЦЕНОК -----
class GradeBase(BaseModel):
    student_id: int  # ID студента
    discipline_id: int  # ID дисциплины
    score: float  # оценка


class GradeOut(GradeBase):
    id: int

    class Config:
        from_attributes = True