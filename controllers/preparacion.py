from flask_restful import Resource,reqparse
from conexion_bd import base_de_datos
from sqlalchemy.exc import IntegrityError
from models.preparacion import PreparacionModel

class PreparacionesController(Resource):
    serializador=reqparse.RequestParser(bundle_errors=True)
    serializador.add_argument(
        'orden',
        type=int,
        location='json',
        required=True,
        help='Fata el orden'
    )
    serializador.add_argument(
        'descripcion',
        type=str,
        location='json',
        required=True,
        help='Falta la descripcion'
    )
    serializador.add_argument(
        'receta_id',
        type=int,
        location='json',
        required=True,
        help='Falta el id de la receta'
    )
    def post(self):

        try:
            data=self.serializador.parse_args()
            print(data)
            nuevaPreparacion=PreparacionModel(preparacionOrden=data.get('orden'),preparacionDescripcion=data.get('descripcion'),receta=data.get('receta_id'))
            print(nuevaPreparacion)
            base_de_datos.session.add(nuevaPreparacion)
            base_de_datos.session.commit()
            json={
                "id":nuevaPreparacion.preparacionId,
                "orden":nuevaPreparacion.preparacionOrden,
                "descripcion":nuevaPreparacion.preparacionDescripcion,
                "receta_id":nuevaPreparacion.receta
            }
            return {
                "content":json,
                "message":"Preparacion creada exitosamente"
            },201

        except IntegrityError  as err:
            return {
                "content":None,
                "message":"receta no existe"
            }

class PreparacionController(Resource):
    def get(sefl,id):
        try:
            preparacion=base_de_datos.session.query(PreparacionModel).filter_by(preparacionId=id).first()
            print(preparacion)
            if preparacion is None:
                raise Exception("Preparacion no existe")
            preparacionDict=preparacion.__dict__.copy()
            del preparacionDict['_sa_instance_state']
            return {
                "content":preparacionDict,
                "message":None
            }
        except Exception as err:
            return {
                "content":None,
                "message":err.args[0]
            }