from flask_restful import Resource,reqparse
from conexion_bd import base_de_datos

from models.receta_ingrediente import RecetaIngredienteModel
from models.receta import RecetaModel
from models.ingrediente import IngredienteModel
from models.log import LogModel

class RecetaIngredienteController(Resource):
    serializador=reqparse.RequestParser(bundle_errors=True)
    serializador.add_argument(
        'receta_id',
        type=int,
        required=True,
        location='json',
        help='Falta la receta_id'
    )
    serializador.add_argument(
        'ingrediente_id',
        type=list,
        location='json',
        required=True,
        help='Falta el ingrediente_id'

    )
    serializador.add_argument(
        'cantidad',
        type=str,
        location='json',
        required=True,
        help="Falta la cantidad"
    )
    def post(self):
        data=self.serializador.parse_args()
        receta_id=data.get('receta_id')
        ingredientes_id=data['ingrediente_id']
        cantidad=data['cantidad']
        try:
            receta=base_de_datos.session.query(RecetaModel).filter(RecetaModel.recetaId==receta_id).first()
            if receta is None:
                raise Exception("Receta no existe")
            
            for ingrediente in ingredientes_id:

                ingredienteEncontrado=base_de_datos.session.query(IngredienteModel).filter(IngredienteModel.ingredienteId==ingrediente).first()
                print(ingredienteEncontrado)

                if ingredienteEncontrado is None:
                    raise Exception("Ingrediente no existe")
                
                nueva_receta_ingrediente=RecetaIngredienteModel(receta=receta_id,ingrediente=ingrediente,recetaIngredienteCantidad=cantidad)

                base_de_datos.session.add(nueva_receta_ingrediente)
            base_de_datos.session.commit()
            return {
                "content":data,
                "message":"Receta Ingrediente Agregado Exitosamente"
            },201
        except Exception as err:
            base_de_datos.session.rollback()
            nuevoLog=LogModel(logRazon=err.args[0])
            base_de_datos.session.add(nuevoLog)
            base_de_datos.session.commit()

            print(err.args)
            return {
                "message":err.args[0],
                "Content":None
            },404