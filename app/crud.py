from sqlalchemy.orm import Session
import sqlalchemy as sa
from .models import Alumno
from . import schemas


async def consulta_alumnos(db: Session):
    print(db)
    async with db.open():
        alumnos = await db.execute(sa.select(Alumno))
    return alumnos.scalars()

def consulta_alumno(db: Session, cuenta: int):

    return db.query(Alumno).filter(Alumno.cuenta == cuenta).first()


def alta_alumno(db: Session, cuenta: int, candidato: schemas.SchemaAlumnoIn):
    alumno = Alumno(cuenta=cuenta, **dict(candidato))
    db.add(alumno)
    db.commit()
    db.refresh(alumno)
    return alumno


def baja_alumno(db: Session, alumno: Alumno):
    db.delete(alumno)
    db.commit()
    return True
