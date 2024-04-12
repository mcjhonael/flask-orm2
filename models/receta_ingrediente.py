from conexion_bd import base_de_datos
from sqlalchemy import Column,types
from sqlalchemy.sql.schema import ForeignKey

class RecetaIngredienteModel(base_de_datos.Model):
    __tablename__='recetas_ingredientes'

    recetaIngredienteId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)

    receta=Column(ForeignKey(column='recetas.id',ondelete="RESTRICT"), name='recetas_id',type_=types.Integer,nullable=False)

    ingrediente=Column(ForeignKey(column="ingredientes.id",ondelete="RESTRICT"),  name='ingredientes_id',type_=types.Integer,nullable=False)
    
    recetaIngredienteCantidad=Column(name='cantidad',type_=types.String(length=45),nullable=True)