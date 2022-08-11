from typing import List
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from . import crud
from . import schemas
from .db import get_db, engine
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
        if len(await crud.consulta_alumnos(db=await get_db())) == 0:
            print('Base vacía.')
    else:
        logging.info(" Ya existen datos en la tabla.") 


@app.get("/api/", response_model=List[schemas.SchemaAlumno])
def vuelca_base(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alumnos = crud.consulta_alumnos(db, skip=skip, limit=limit)
    return alumnos


@app.get("/api/{cuenta}", response_model=schemas.SchemaAlumno)
def get_alumno(cuenta, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        return alumno
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.delete("/api/{cuenta}")
def delete_alumno(cuenta, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        crud.baja_alumno(db=db, alumno=alumno)
        return {'message':"OK"}
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.post("/api/{cuenta}", response_model=schemas.SchemaAlumno)
def post_alumno(cuenta, candidato: schemas.SchemaAlumnoIn, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        raise HTTPException(status_code=409, detail="Recurso existente")
    return crud.alta_alumno(db=db, cuenta=cuenta, candidato=candidato)        
        
        
@app.put("/api/{cuenta}", response_model=schemas.SchemaAlumno)
def put_alumno(cuenta, candidato: schemas.SchemaAlumnoIn, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        crud.baja_alumno(db=db, alumno=alumno)
        return crud.alta_alumno(db=db, cuenta=cuenta, candidato=candidato)
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    