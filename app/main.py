from typing import List
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from . import crud
from . import schemas
from .db import engine, session
from .models import Base
from data import DATOS_PRUEBA
import logging
import settings

logging.basicConfig(filename='myapp.log', level=logging.INFO)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
    logging.info(" Base iniciada.")
    if settings.TESTING:
        alumnos = await crud.consulta_alumnos(db=session())
        if len(alumnos) == 0:
            logging.info(' La tabla está vacía.')
            logging.info(' Ingresando datos de prueba...')
            for alumno in DATOS_PRUEBA:
                cuenta = alumno.pop("cuenta")
                await crud.alta_alumno(db=session(), 
                                 cuenta=cuenta, 
                                 candidato=alumno)
            logging.info(' Datos de prueba ingresados.')
        else:
            logging.info(" Ya existen datos en la tabla.") 


@app.get("/api/", response_model=List[schemas.SchemaAlumno])
async def vuelca_base():
    alumnos = await crud.consulta_alumnos(db=session())
    return alumnos


@app.get("/api/{cuenta:int}")
async def get_alumno(cuenta, response_model=schemas.SchemaAlumno):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        return alumno
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

       
@app.delete("/api/{cuenta:int}", status_code=201)
async def delete_alumno(cuenta):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        await crud.baja_alumno(db=session(), alumno=alumno)
        return {'message':"OK"}
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.post("/api/{cuenta:int}", response_model=schemas.SchemaAlumno)
async def post_alumno(cuenta, candidato: schemas.SchemaAlumnoIn):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        raise HTTPException(status_code=409, detail="Recurso existente")
    return await crud.alta_alumno(db=session(), cuenta=cuenta, candidato=candidato)        
        
        
@app.put("/api/{cuenta:int}", response_model=schemas.SchemaAlumno)
async def put_alumno(cuenta, candidato: schemas.SchemaAlumnoIn):
    alumno = await crud.consulta_alumno(db=session(), cuenta=cuenta)
    if alumno:
        await crud.baja_alumno(db=session(), alumno=alumno)
        return await crud.alta_alumno(db=session(), cuenta=cuenta, candidato=candidato)
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")