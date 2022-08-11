from sqlalchemy.orm import Session
from .models import Alumno
from . import schemas
import sqlalchemy as sa

async def consulta_alumnos(db: Session):
    async with db.begin():
        results = await db.execute(sa.select(Alumno))
        return results.scalars().all()


async def consulta_alumno(db: Session, cuenta: int):
    async with db.begin():
        results = await db.execute(sa.select(Alumno).where(Alumno.cuenta == cuenta))
        return results.scalars().first()


async def alta_alumno(db: Session, cuenta: int, candidato: schemas.SchemaAlumnoIn):
    alumno = Alumno(cuenta=cuenta, **dict(candidato))
    async with db.begin():
        db.add(alumno)
    return alumno


async def baja_alumno(db: Session, alumno: Alumno):
    async with db.begin():
        stmnt = sa.delete(Alumno).where(Alumno.cuenta == alumno.cuenta)
        await db.execute(stmnt)
    return True
