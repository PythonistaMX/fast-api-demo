from data import DATOS_PRUEBA
from typing import List
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from . import crud
from . import schemas
from .db import database
import logging
import settings


logging.basicConfig(filename='myapp.log', level=logging.INFO)



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await database.connect() 
    logging.info(" Base iniciada.")
    if settings.TESTING:
        alumnos = await crud.consulta_alumnos()
        if len(alumnos) == 0:
            logging.info(' La tabla está vacía.')
            logging.info(' Ingresando datos de prueba...')
            for alumno in DATOS_PRUEBA:
                cuenta = alumno.pop("cuenta")
                await crud.alta_alumno(cuenta=cuenta, 
                                       candidato=alumno)
            logging.info(' Datos de prueba ingresados.')
        else:
            logging.info(" Ya existen datos en la tabla.") 


@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect() 

@app.get("/api/", response_model=List[schemas.SchemaAlumno])
async def vuelca_base():
    alumnos = await crud.consulta_alumnos()
    return alumnos


@app.get("/api/{cuenta}")
async def get_alumno(cuenta, response_model=schemas.SchemaAlumno):
    alumno = await crud.consulta_alumno(cuenta=cuenta)
    if alumno:
        return alumno
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.delete("/api/{cuenta}", status_code=201)
async def delete_alumno(cuenta):
    alumno = await crud.consulta_alumno(cuenta=cuenta)
    if alumno:
        await crud.baja_alumno(cuenta=cuenta)
        return {'message':"OK"}
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.post("/api/{cuenta}", response_model=schemas.SchemaAlumno)
async def post_alumno(cuenta, candidato: schemas.SchemaAlumnoIn):
    alumno = await crud.consulta_alumno(cuenta=cuenta)
    if alumno:
        raise HTTPException(status_code=409, detail="Recurso existente")
    else:
        return await crud.alta_alumno(cuenta=cuenta, candidato=dict(candidato))        
        
        
@app.put("/api/{cuenta}", response_model=schemas.SchemaAlumno)
async def put_alumno(cuenta, candidato: schemas.SchemaAlumnoIn):
    alumno = await crud.consulta_alumno(cuenta=cuenta)
    if alumno:
        await crud.baja_alumno(cuenta=cuenta)
        return await crud.alta_alumno(cuenta=cuenta, candidato=dict(candidato))
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    