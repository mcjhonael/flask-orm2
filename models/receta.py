from conexion_bd import base_de_datos
from sqlalchemy import Column,types,orm
from enum import Enum

class EnumPorcion(Enum):
    personal='personal'
    mediano='mediano'
    familiar='familiar'

class RecetaModel(base_de_datos.Model):
    __tablename__="recetas"

    recetaId=Column(name=   'id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)
    
    recetaNombre=Column(name='nombre',type_=types.String(length=255),nullable=True)
    
    recetaPorcion=Column(name='porcion',type_=types.Enum(EnumPorcion))
    

    # aqui se van almacenar todas las preparacion de dicha receta que yo ando buscando
    # yo desde mi tabla receta preparacion puedo acceder a todas las preparaciones
    # reacuerda que dentro de la tabla preparacion se encuentra un atributo llamado preparacionRecetasz
    preparaciones=orm.relationship('PreparacionModel',backref='preparacionRecetas',lazy=True)
    
    recetas_ingredientes=orm.relationship('RecetaIngredienteModel',backref='recetasIngredienteRecetas',lazy=True)