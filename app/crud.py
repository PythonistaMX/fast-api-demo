from .db import database, tabla_alumnos
from . import schemas

async def consulta_alumnos():
    query = tabla_alumnos.select()
    return await database.fetch_all(query)


async def consulta_alumno(cuenta: int):
    # query = "SELECT * FROM alumnos WHERE cuenta = :cuenta"
    query = tabla_alumnos.select().where(tabla_alumnos.c.cuenta == cuenta)
    values = {'cuenta': cuenta}
    return await database.fetch_one(query=query) # values=values)


async def alta_alumno(cuenta: int, candidato: schemas.SchemaAlumnoIn):
    candidato['cuenta'] = cuenta
    query = tabla_alumnos.insert()
    await database.execute(query=query, values=candidato)
    return candidato


async def baja_alumno(cuenta: int):
    query = tabla_alumnos.delete().where(tabla_alumnos.c.cuenta == cuenta)
    await database.execute(query=query)
    return True
