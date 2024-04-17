from flask_restful import Resource, reqparse
from conexion_bd import base_de_datos
from sqlalchemy.exc import IntegrityError, DataError


# import models
from models.ingrediente import IngredienteModel
from models.log import LogModel


serializador = reqparse.RequestParser()
serializador.add_argument(
    'nombre',
    type=str,
    required=True,
    location='json',
    help='Falta el nombre'
)


class IngredientesController(Resource):
    def get(self):
        #  data=IngredienteModel.query.all()
        #  print(data)

        ingredientes = base_de_datos.session.query(IngredienteModel).all()
        print(ingredientes)

        resultado = []

        for ingrediente in ingredientes:
            # print(ingrediente.__dict__)
            ingrediente_dicc = ingrediente.__dict__
            del ingrediente_dicc['_sa_instance_state']
            print(ingrediente_dicc)
            resultado.append({
                "id": ingrediente.ingredienteId,
                "nombre": ingrediente.ingredienteNombre
            })
        print(resultado)
        return {
            "content": resultado,
            "message": None
        }

    def post(self):
        data = serializador.parse_args()
        # print(data)
        try:
            nuevoIngrediente = IngredienteModel(
                ingredienteNombre=data['nombre'])
            base_de_datos.session.add(nuevoIngrediente)
            base_de_datos.session.commit()
            print(nuevoIngrediente)
            json = {
                "id": nuevoIngrediente.ingredienteId,
                "nombre": nuevoIngrediente.ingredienteNombre
            }
            error = None
            return {
                "content": json,
                "message": "Ingrediente Creado exitosamente"
            }, 201
        except IntegrityError as err:
            error = err
            return {
                "message": "El ingrediente ya existe"
            }, 500
        except DataError as err:
            error = err
            return {
                "message": "Error al ingresar el ingrediente"
            }, 500
        except Exception as err:
            error = err
            return {
                "message": "Error Desconocido"
            }, 500
        finally:
            if error is None:
                return {
                    "content": json,
                    "message": "Ingrediente Creado exitosamente"
                }, 201
            else:
                base_de_datos.session.rollback()
                nuevoLog=LogModel()
                print(f' mi errorcito{error.args[0]}')
                nuevoLog.logRazon=error.args[0]
                base_de_datos.session.add(nuevoLog)
                base_de_datos.session.commit()

class IngredienteController(Resource):
    def get(self,id):
        resultado2=base_de_datos.session.query(IngredienteModel).filter_by(ingredienteId=id).first()
        print(resultado2)
        if resultado2 is None:
            return {
                "content":None,
                "message":"Ingrediente no encontrado"
            },404
        data=resultado2.__dict__
        del data["_sa_instance_state"]
        json={
            "id":data.get('ingredienteId'),
            "nombre":data.get('ingredienteNombre')
        }
        print(json)
        return {
            "content":json,
            "message":"Ingrediente encontrado"
        },200

    def put(self,id):
        data=serializador.parse_args()
        ingrediente=base_de_datos.session.query(IngredienteModel).filter_by(ingredienteId=id).first()
        if ingrediente is None:
            return {
                "content":None,
                "message":"Ingrediente no existe"
            },404
        ingrediente.ingredienteNombre=data.get("nombre")
        respuesta=ingrediente.__dict__.copy()
        base_de_datos.session.commit()
        del respuesta['_sa_instance_state']
        return {
            "content":respuesta,
            "message":"Ingrediente actuatizado"
        },201
    def delete(self,id):
        # base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId==id).delete()
        # entonces siempre debemos usar un try catch cuando hagamos crud siempreeeeeee
        try:
            ingrediente=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId==id).first()
            base_de_datos.session.delete(ingrediente)
            base_de_datos.session.commit()
            return {
                "message":"Ingrediente eliminado",
                "content":None
            },204
        except:
            return {
                "content":None,
                "message":"Error al eliminar el ingrediente"
            },500

serializadorFiltro=reqparse.RequestParser()
serializadorFiltro.add_argument(
    'nombre',
    type=str,
    required=True,
    location='args',
    help="no se encontro en el buscador"
)
class FiltroIngredientesController(Resource):
    def get(self):
        filtro=serializadorFiltro.parse_args()
        resultado=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteNombre.like('%{}%'.format(filtro['nombre']))).all()
        print(resultado)

        resultado_final=[]
        for registro in resultado:
            ingrediente_dicc=registro.__dict__.copy()
            del ingrediente_dicc['_sa_instance_state']
            resultado_final.append({
                "id":ingrediente_dicc['ingredienteId'],
                "nombre":ingrediente_dicc['ingredienteNombre']
            })
        return{
            "contento":resultado_final,
            "message":"Todos los ingredientes"
        }
        print(resultado_final)