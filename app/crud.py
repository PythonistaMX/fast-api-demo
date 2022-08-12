from .db import database, tabla_alumnos
from . import schemas
import sqlalchemy as sa

async def consulta_alumnos():
    query = tabla_alumnos.select()
    return await database.fetch_all(query)


async def consulta_alumno(cuenta: int):
    query = tabla_alumnos.select(values={"cuenta": cuenta})
    return await database.fetch_one(query=query)


async def alta_alumno(cuenta: int, candidato: schemas.SchemaAlumnoIn):
    candidato['cuenta'] = cuenta
    query = tabla_alumnos.insert()
    await database.execute(query=query, values=candidato)
    return candidato


async def baja_alumno(cuenta):
    query = tabla_alumnos.delete()
    await database.execute(query=query, values={"cuenta": cuenta})
    return True
