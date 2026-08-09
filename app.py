from datetime import date
from flask import Flask, render_template  
from flask_sqlalchemy import SQLAlchemy
# Esta linea importa las herramientas necesarias de la libreria flask que isntalamos
# Flask: es el q conveirte el archivo Python en un servidor de web
# render_template: es una funcion especial de Flask q se encarga de tomar un archivo HTML y lo envia al navegador del usuario

app = Flask(__name__)
# Crea la aplicacion web y la guarda dentro de la variable app
# __name__: es una variable especial de Python. Le indica a Flask donde esta ubicado este archivo dentro de tu proyecto para q sepa dodne buscar las imagenes, estilos y paginas HTML cuando las necesite

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
# Le estamos diciendo al Flask q a partir de ahora, todos los habitos q el usuario cree, modifique o borre, los va a ir guardando de forma permanente adentro de un archivo llamado habits.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-password-secret-key'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all() 



@app.route('/')
# Crea una ruta (una pagina web)
def index():
    return render_template('index.html')

# Ruta de los Hábitos
@app.route("/habits")
def habits():
    return render_template("habits.html")

# Ruta de las Estadísticas
@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


if __name__ == '__main__':
    app.run(debug=True)
