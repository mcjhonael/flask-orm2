from conexion_bd import base_de_datos
from sqlalchemy import Column,types
from sqlalchemy.sql.schema import ForeignKey

class PreparacionModel(base_de_datos.Model):
    __tablename__="preparaciones"

    preparacionId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)

    preparacionOrden=Column(name='orden',type_=types.Integer,nullable=True,default=1)
    
    preparacionDescripcion=Column(name='descripcion',type_=types.Text,nullable=True)

    receta=Column(ForeignKey(column='recetas.id' ,ondelete='RESTRICT'), name='recetas_id',type_=types.Integer,nullable=False)
    
    def __str__(self):
        return f'Mi Preperacion es {self.preparacionOrden}'
    