from flask_restful import Resource,reqparse
from conexion_bd import base_de_datos
from sqlalchemy.exc import IntegrityError

from models.preparacion import PreparacionModel
from models.receta import RecetaModel

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
#^OJO CREAMOS UN VINCULO CON RECETA Y PREPARACIONES POR QUE CUANDO YO TENGA LA TABLA PREPARACIONES AHI DEBE SALIR LA LISTA DE PREPARACIONES O LISTA DE PASOS PARA HACER LAS PREPARACIONES INCLUIDO CON SU RECETA A LA CUAL CORRESPONDE 
# ! Y CUANDO YO LLAME UNA RECETA ESTA DEBE MOSTRARME TBM LA LISTA DE PREPARACIONES QUE YO DEBO SEGUIR PARA HACER ESA RECETA ENTENDISTE X ESO SE CREA UNA RELACION DE TIPO ORM.RELATIONSHIP
# *en el modelo RecetaModel creo una variable ficticia llamada preparaciones la cual va almacenar todas las preparaciones y
class PreparacionController(Resource):
    def get(self,id):
        try:
            preparacion=base_de_datos.session.query(PreparacionModel).filter_by(preparacionId=id).first()
            if preparacion is None:
                raise Exception("Preparacion no existe")
            preparacionDict=preparacion.__dict__.copy()
            del preparacionDict['_sa_instance_state']

            # esto solo es una prueba amiguitos nada importante pero si
            print(preparacion.receta)

            recetitas=base_de_datos.session.query(RecetaModel).filter(RecetaModel.recetaId==preparacion.receta).first()
            recetaEncontrada=recetitas.__dict__.copy()
            del recetaEncontrada['_sa_instance_state']
            recetaEncontrada['recetaPorcion']=recetitas.recetaPorcion.value

            json={
                "id":preparacionDict['preparacionId'],
                "orden":preparacionDict['preparacionOrden'],
                "descripcion":preparacionDict['preparacionDescripcion'],
                "receta":{
                    "id":recetaEncontrada['recetaId'],
                    "nombre":recetaEncontrada['recetaNombre'],
                    "porcion":recetaEncontrada['recetaPorcion']
                }
            }
            return {
                "content":json,
                "message":None
            }
        except Exception as err:
            return {
                "content":None,
                "message":err.args[0]
            }