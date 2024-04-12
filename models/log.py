from conexion_bd import base_de_datos
from sqlalchemy import Column,types
from datetime import datetime

class LogModel(base_de_datos.Model):
    __tablename__="logs"

    logId=Column(name='id',type_=types.Integer ,primary_key=True,autoincrement=True,nullable=False,unique=True)
# hace un llamado ala funcion utcnow si ponemos () entonces ejecutar a la funcion x lo cual cuando ingremos otros registros llamara a esa misma hora doende se ejecuto lo cual sera erroneo xk siempre se modifica x eso lo referenciamos no lo ejecutamos
    logFecha=Column(name='fecha',type_=types.DateTime(),default=datetime.utcnow)

    logRazon=Column(name='razon',type_=types.Text,nullable=True)