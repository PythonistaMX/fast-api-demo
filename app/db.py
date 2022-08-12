import sqlalchemy as sa
import databases
from settings import SQLALCHEMY_DATABASE_URL

database = databases.Database(SQLALCHEMY_DATABASE_URL)

metadata = sa.MetaData()

tabla_alumnos = sa.Table(
                        "alumnos",
                        metadata,
                        sa.Column('cuenta', sa.Integer, primary_key=True),
                        sa.Column('nombre', sa.String(50)),
                        sa.Column('primer_apellido', sa.String(50)),
                        sa.Column('segundo_apellido', sa.String(50)),
                        sa.Column('carrera', sa.String(50)),
                        sa.Column('semestre', sa.Integer),
                        sa.Column('promedio', sa.Float),
                        sa.Column('al_corriente', sa.Boolean))

engine = sa.create_engine(SQLALCHEMY_DATABASE_URL)

metadata.create_all(engine)
