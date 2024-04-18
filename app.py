from flask import Flask
from conexion_bd import base_de_datos

#import models
from models.ingrediente import IngredienteModel
from models.receta import RecetaModel
from models.preparacion import PreparacionModel
from models.receta_ingrediente import RecetaIngredienteModel
from models.log import LogModel

#import controllers
from controllers.ingrediente import IngredientesController,IngredienteController,FiltroIngredientesController

from controllers.receta import RecetasController,RecetaController

from controllers.preparacion import PreparacionesController,PreparacionController

from controllers.receta_ingrediente import RecetaIngredienteController


from dotenv import load_dotenv
from os import environ
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint


load_dotenv()

# es una ruta standar para nuestras api siempre usar eso
SWAGGER_URL = '/api/docs' 
# ruta donde se encuentra mi archivo swagger.json
API_URL='./static/swagger.json'

swaggerui_blueprint=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Resposteria Flask - Documentacion Swagger'
    }
)


app = Flask(__name__)

# blueprint = sirve para registar en el caso de nosotros tengamos un proyecto internoy queramos agregarlo al proyecto principal de Flask como microservicios 
app.register_blueprint(swaggerui_blueprint)

# con origins indicamos que pagina puede acceder a nuestra api x ejemplo http://pacolo.com solo el puede acceder a nuestra api nadie mas. los methods que se puede consultar en la api
CORS(app=app,methods=['GET','POST','PUT','DELETE'],origins='*',allow_headers='*')

api=Api(app)

# area de configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# area de inicializara la db
base_de_datos.init_app(app)
Migrate(app=app,db=base_de_datos)

# print(app.config)
# # Asi utilizariamos la creacion de las tablas sin utilizar migraciones
# este controlador se ejecutara antes del primer request de nuestro servidor
# @app.before_first_request
# def inicializadora():
    # realizar la creacion de todos los modelos de nuestro proyecto como tablas en la base de datos
    # base_de_datos.create_all()
    # pass


# Zona de enrutamiento
api.add_resource(IngredientesController,'/ingredientes')
api.add_resource(IngredienteController,'/ingrediente/<int:id>')

api.add_resource(FiltroIngredientesController,'/buscar_ingrediente')

api.add_resource(PreparacionesController,'/preparaciones')
api.add_resource(PreparacionController,'/preparacion/<int:id>')

api.add_resource(RecetasController,'/recetas')
api.add_resource(RecetaController,'/receta/<int:id>')

api.add_resource(RecetaIngredienteController,'/recetas_ingredientes')
@app.route('/', methods=['GET'])
def initial_controller():
    return {
        "content": "",
        "message": "MI API DE RESPOSTERIA"
    }

if __name__ == '__main__':

    app.run(port=2000, debug=True)
# https://www.apimatic.io/ se encarga de transformar nuestro archivo postman que fue exportado a un archivo swagger 
#  dentro de apimatic vamos a transform API y cargamos el archivo para ello lo cargamos y despues no debe salir OpenAPI/Swagger v2.0(JSON)
# y nos va descargar un archivo swagger 
# https://editor.swagger.io/ esta pagina sirve para editar nuestro archivo swagger por algyunas cosas que faltan editor en linea swagger
# lo arrastramos y empezamos a editar