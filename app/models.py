import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Alumno(Base):
    '''Modelo de alumnos.'''
    __tablename__ = 'alumnos'
    cuenta = sa.Column(sa.Integer, primary_key=True)
    nombre = sa.Column(sa.String(50))
    primer_apellido = sa.Column(sa.String(50))
    segundo_apellido = sa.Column(sa.String(50))
    carrera = sa.Column(sa.String(50))
    semestre = sa.Column(sa.Integer)
    promedio = sa.Column(sa.Float)
    al_corriente = sa.Column(sa.Boolean)