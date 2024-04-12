from flask_restful import Resource, reqparse
from conexion_bd import base_de_datos
from models.receta import RecetaModel
from math import ceil


class RecetasController(Resource):
    serializador = reqparse.RequestParser()

    def post(self):
        self.serializador.add_argument(
            'nombre',
            type=str,
            location='json',
            required=True,
            help='Ingre el nombre de la receta'
        )
        self.serializador.add_argument(
            'porcion',
            type=str,
            location='json',
            required=True,
            help='Seleccione la porcion',
            choices=['personal', 'mediano', 'familiar']
        )
        try:
            data = self.serializador.parse_args()
            print(data)
            nuevaReceta = RecetaModel(recetaNombre=data.get(
                'nombre'), recetaPorcion=data.get('porcion'))
            base_de_datos.session.add(nuevaReceta)
            base_de_datos.session.commit()
            return {
                "content": data,
                "message": "Receta Creada exitosamente"
            }, 201
        except:
            print("Hubo un error al guardar la receta, intentalo de nuevo")

    def get(self):
        self.serializador.add_argument(
            'page',
            type=int,
            required=True,
            location='args',
            help='falta la cantidad de paginas',
        )
        self.serializador.add_argument(
            'perPage',
            type=int,
            location='args',
            required=True,
            help='por paginas a mostrar'
        )
        data = self.serializador.parse_args()

        page = data['page']
        perPage = data['perPage']
        limit = perPage
        offset = (page-1)*limit
        totalRecetas = base_de_datos.session.query(RecetaModel).count()
        print(f'total de recetas {totalRecetas}')

        itemsPorPagina = perPage if totalRecetas >= perPage else None
        print(f' cantidad de paginas {itemsPorPagina}')
        totalPaginas = ceil(totalRecetas/itemsPorPagina)
        print(f' la pagina es  {totalPaginas}')
        if page > 1:
            paginaPrevia = page-1 if page <= totalPaginas else None
        else:
            paginaPrevia = None
        if totalPaginas > 1:
            paginaSiguiente = page+1 if page < totalPaginas else None
        else:
            paginaSiguiente = None

        recetas = base_de_datos.session.query(
            RecetaModel).limit(limit).offset(offset).all()
        resultado = []
        for receta in recetas:
            recetaDict = receta.__dict__.copy()
            del recetaDict['_sa_instance_state']
            recetaDict['recetaPorcion'] = recetaDict['recetaPorcion'].value
            resultado.append(recetaDict)
        return {
            "content": resultado,
            "pagination": {
                "total": totalRecetas,
                "perPages": itemsPorPagina,
                "paginaPrevia": paginaPrevia,
                "paginaSiguiente": paginaSiguiente,
                "totalPaginas": totalPaginas
            }
        }

class RecetaController(Resource):
    # ? OJO RECUERDA CUANDO YO QUIERO MOSTRAR 1 RECETA ESTA DEBE MOSTRAR TAMBIEN SU PREPARACION ES LOGICA
    # ?EL RELTIONSHIP SIRVE PARA INDICAR LOS HIJOS QE PUEDE TENER ESE MODELO CON ALGUNAS RELACIONES PREVIAMENTE DECLARADAS NO PUEDE SER SI NO ESTAN UNIDAD SI O SI DEBE HABER UNA RELACION 
    # ?BACKREF CREA UN ATRIBUTO VIRTUAL DENTRO DEL MODELO PREPARACIONMODEL LO CUALSIRVE PARA ACCEDER A TODO EL OBJETO INVERSO SIN LA NECESIDAD DE HACER UN JOIN NI NADA DE ESO SI NO DEFRENTE EN ESE ATRIBUTO
    # ?el nombre debe estar en funcion a sus nombre de tus atributos
    # PREAPRACIONES A RECETAS ENTONCES USAMOS PREPARACIONRECETAS Y CUANDO ES QUERAMOS DE RECETA A PREPARACIONES USAMOS PREPARACIONES TODO ESTO ESTA EN EL MODELO RECETAMODEL 
    # receta es una tabla padre que puede tener muchos hijos como preparaciones,
    # una preapracion solo tiene 1 receta 
    # creamos un atributo preapraciones que seria el relationship 
    def get(self,id):
        receta=base_de_datos.session.query(RecetaModel).filter(RecetaModel.recetaId==id).first()

        print(receta.recetaNombre)
        print(receta.preparaciones)