from conexion_bd import base_de_datos
from sqlalchemy import Column,types,orm

class IngredienteModel(base_de_datos.Model):
    __tablename__="ingredientes"

    ingredienteId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)
    
    ingredienteNombre=Column(name='nombre',type_=types.String(length=45),nullable=True,unique=True)

    recetas_ingredientes=orm.relationship('RecetaIngredienteModel',backref='recetaIngredienteIngredientes',lazy=True)

    def __str__(self):
        return 'EL INGREDIENTES %s' % (self.ingredienteNombre)
    