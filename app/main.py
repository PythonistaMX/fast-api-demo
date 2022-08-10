from typing import List
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from . import crud
from . import models
from . import schemas
from .db import SessionLocal, engine
from .models import Alumno
from data import DATOS_PRUEBA

import logging
import settings

logging.basicConfig(filename='myapp.log', level=logging.INFO)

app = FastAPI()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)
    logging.info(" Base iniciada.")
    if settings.TESTING:
        if len(db.query(Alumno).filter(Alumno.cuenta).all()) == 0:
            logging.info(" Ingresando datos de prueba.")
            for alumno in DATOS_PRUEBA:
                db.add(Alumno(**alumno))
            db.commit()
        else:
           logging.info(" Ya existen datos en la tabla.") 


@app.get("/api/", response_model=List[schemas.SchemaAlumno])
async def vuelca_base(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alumnos = crud.consulta_alumnos(db, skip=skip, limit=limit)
    return alumnos


@app.get("/api/{cuenta}", response_model=schemas.SchemaAlumno)
async def get_alumno(cuenta, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        return alumno
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.delete("/api/{cuenta}")
async def delete_alumno(cuenta, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        crud.baja_alumno(db=db, alumno=alumno)
        return {'message':"OK"}
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")

        
@app.post("/api/{cuenta}", response_model=schemas.SchemaAlumno)
async def post_alumno(cuenta, candidato: schemas.SchemaAlumnoIn, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        raise HTTPException(status_code=409, detail="Recurso existente")
    return crud.alta_alumno(db=db, cuenta=cuenta, candidato=candidato)        
        
        
@app.put("/api/{cuenta}", response_model=schemas.SchemaAlumno)
async def put_alumno(cuenta, candidato: schemas.SchemaAlumnoIn, db: Session = Depends(get_db)):
    alumno = crud.consulta_alumno(db=db, cuenta=cuenta)
    if alumno:
        crud.baja_alumno(db=db, alumno=alumno)
        return crud.alta_alumno(db=db, cuenta=cuenta, candidato=candidato)
    else:
        raise HTTPException(status_code=404, detail="Recurso no encontrado")
    
    