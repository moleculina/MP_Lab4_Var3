# routes.py - все адреса, по которым можно обращаться к серверу

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from . import models, schemas
from .database import get_db

# Создаём маршрутизатор (все адреса будут начинаться с /api)
router = APIRouter(prefix="/api", tags=["university"])


# ==========================================
# ============== СТУДЕНТЫ ==================
# ==========================================

@router.get("/students", response_model=List[schemas.StudentOut])
def get_students(db: Session = Depends(get_db)):
    """
    ПОЛУЧИТЬ СПИСОК ВСЕХ СТУДЕНТОВ
    Адрес: GET /api/students
    """
    # Запрашиваем всех студентов из БД
    students = db.query(models.Student).all()

    result = []
    for student in students:
        # Вычисляем средний балл каждого студента
        avg = db.query(func.avg(models.Grade.score)).filter(
            models.Grade.student_id == student.id
        ).scalar()

        result.append(schemas.StudentOut(
            id=student.id,
            name=student.name,
            group=student.group,
            average_score=avg
        ))
    return result


@router.post("/students", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    ДОБАВИТЬ НОВОГО СТУДЕНТА
    Адрес: POST /api/students
    """
    # Создаём нового студента
    db_student = models.Student(name=student.name, group=student.group)
    db.add(db_student)  # Добавляем в базу
    db.commit()  # Сохраняем изменения
    db.refresh(db_student)  # Обновляем (чтобы получить ID)

    return schemas.StudentOut(
        id=db_student.id,
        name=db_student.name,
        group=db_student.group
    )


@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    УДАЛИТЬ СТУДЕНТА
    Адрес: DELETE /api/students/{id}
    """
    # Ищем студента в базе
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    db.delete(student)  # Удаляем
    db.commit()  # Сохраняем
    return {"ok": True}


# ==========================================
# ============== ДИСЦИПЛИНЫ ================
# ==========================================

@router.get("/disciplines", response_model=List[schemas.DisciplineOut])
def get_disciplines(db: Session = Depends(get_db)):
    """
    ПОЛУЧИТЬ СПИСОК ВСЕХ ДИСЦИПЛИН
    Адрес: GET /api/disciplines
    """
    return db.query(models.Discipline).all()


@router.post("/disciplines", response_model=schemas.DisciplineOut)
def create_discipline(discipline: schemas.DisciplineCreate, db: Session = Depends(get_db)):
    """
    ДОБАВИТЬ НОВУЮ ДИСЦИПЛИНУ
    Адрес: POST /api/disciplines
    """
    db_disc = models.Discipline(name=discipline.name, credits=discipline.credits)
    db.add(db_disc)
    db.commit()
    db.refresh(db_disc)
    return db_disc


# ==========================================
# ============== ОЦЕНКИ ====================
# ==========================================

@router.post("/grades", response_model=schemas.GradeOut)
def add_grade(grade: schemas.GradeBase, db: Session = Depends(get_db)):
    """
    ПОСТАВИТЬ ОЦЕНКУ
    Адрес: POST /api/grades
    """
    db_grade = models.Grade(
        student_id=grade.student_id,
        discipline_id=grade.discipline_id,
        score=grade.score
    )
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


# ==========================================
# ========== СПЕЦИАЛЬНЫЕ ЗАПРОСЫ ============
# ==========================================

@router.get("/top-students")
def top_students(db: Session = Depends(get_db)):
    """
    ТОП-5 ЛУЧШИХ СТУДЕНТОВ
    Адрес: GET /api/top-students
    """
    results = db.query(
        models.Student.id,
        models.Student.name,
        models.Student.group,
        func.avg(models.Grade.score).label("avg_score")
    ).join(models.Grade).group_by(models.Student.id).order_by(
        func.avg(models.Grade.score).desc()
    ).limit(5).all()

    return [
        {
            "id": r[0],
            "name": r[1],
            "group": r[2],
            "average_score": float(r[3])
        } for r in results
    ]


@router.get("/discipline-rating/{discipline_id}")
def discipline_rating(discipline_id: int, db: Session = Depends(get_db)):
    """
    РЕЙТИНГ СТУДЕНТОВ ПО КОНКРЕТНОЙ ДИСЦИПЛИНЕ
    Адрес: GET /api/discipline-rating/{id}
    """
    # Сначала проверяем, существует ли такая дисциплина
    disc = db.query(models.Discipline).filter(models.Discipline.id == discipline_id).first()

    if not disc:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")

    # Получаем всех студентов с их оценками по этой дисциплине
    results = db.query(
        models.Student.name,
        models.Grade.score
    ).join(models.Grade).filter(
        models.Grade.discipline_id == discipline_id
    ).order_by(models.Grade.score.desc()).all()

    return {
        "discipline": disc.name,
        "students": [{"name": r[0], "score": r[1]} for r in results]
    }


@router.get("/honors-students")
def honors_students(db: Session = Depends(get_db)):
    """
    НАЙТИ ОТЛИЧНИКОВ (средний балл >= 4.5)
    Адрес: GET /api/honors-students
    """
    results = db.query(
        models.Student.id,
        models.Student.name,
        models.Student.group,
        func.avg(models.Grade.score).label("avg_score")
    ).join(models.Grade).group_by(models.Student.id).having(
        func.avg(models.Grade.score) >= 4.5
    ).all()

    return [
        {
            "id": r[0],
            "name": r[1],
            "group": r[2],
            "average_score": float(r[3])
        } for r in results
    ]