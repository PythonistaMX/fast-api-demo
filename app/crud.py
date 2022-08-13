from sqlalchemy.orm import Session
from .models import Alumno
from .schemas import SchemaAlumnoIn
import sqlalchemy as sa


async def consulta_alumnos(db: Session):
    async with db.begin():
        stmnt = sa.select(Alumno)
        results = await db.execute(stmnt)
        return results.scalars().all()


async def consulta_alumno(db: Session, cuenta: int):
    async with db.begin():
        stmnt = sa.select(Alumno).where(Alumno.cuenta == cuenta)
        results = await db.execute(stmnt)
        return results.scalars().first()


async def alta_alumno(db: Session, cuenta: int, candidato: SchemaAlumnoIn):
    alumno = Alumno(cuenta=cuenta, **dict(candidato))
    async with db.begin():
        db.add(alumno)
    return alumno


async def baja_alumno(db: Session, alumno: Alumno):
    async with db.begin():
        stmnt = sa.delete(Alumno).where(Alumno.cuenta == alumno.cuenta)
        await db.execute(stmnt)
    return True