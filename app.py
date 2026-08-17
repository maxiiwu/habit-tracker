from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

# 1. Crear la aplicacion
app = Flask(__name__)
# Hace q el archivo Python se convierta en un servidor web q se peuda ver en el navegador

# 2. Le decimos a Flask donde se va a crear la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
# habits.db es como un archivo de Excel gigante
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Conectar la base de datos a la app
db = SQLAlchemy(app)

# Estamos creando un Modelo. Le estamos ensenando a la base de datos que significa exactamente un "Habito" para nosotoras
class Habito(db.Model):  # asi es como le decimos a Python como disenar las columnas d esa tabla Excel
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    completado = db.Column(db.Boolean, default = False)
# id: nro unico para q la base de datos no confunda "Tomar agua" de la manana con "Tomar agua" de la tarde
# nombre: el texto en si
# estado: interruptor para saber si ya lo completaste hoy
# db.Column == "database Column" --> le avisa a SQLAlchemy que la variable q estamos definiendo (id, nombre, completado) va a ser una columna dentro de nuestra tabla
# db.Integer: configuramos para q esa celda acepte solo nros enteros
# db.String: configuramos para q esa celde acepte solo string (con 100 siendo el limite max de caracteres permitidos)
# db.Boolean: configuramos para q sea solo un bool. El habito puede estar: completado (completado = True) o pendiente (completado = False)
# primary_key = True: le dice a Python q no se repitan las cosas. Asiq si tenemos un habito "Leer" y despues otro habit "Leer", la base de datos va a saber q son diferentes
# nullable = False: le prohibe a la base de datos guardar un habito donde no tenia nada escrito
# default = False: si agregas un habito nuevo y te olvidas de avisarle si ya fue completado, automaticamente asume q todavia no lo hiciste

with app.app_context():
    db.create_all()


@app.route("/")
def inicio():
    lista_habitos = Habito.query.all()
    return render_template("index.html", habitos = lista_habitos)

@app.route("/agregar", methods = ["POST"])  # Le decimos a Flask, q esta ruta solo acepta envio de datos (POST)
def agregar_habito():
    nombre_nuevo = request.form.get("nombre_habito")  
    # nombre_habito es el name q le pusimos al input

    nuevo_habito = Habito(nombre = nombre_nuevo)
    # Creamos un nuevo objeto Habito con ese nombre

    db.session.add(nuevo_habito)
    db.session.commit()  # Es el equivalente a hacer "Guardar archivo" en un Excel
    # Lo agregamos a la base de datos y guardamos los cambios

    return redirect(url_for("inicio"))
    # Lo redireccionamos a la pagina ppal para ver la lista actualizada

@app.route("/completar/<int:id>")
def completar_habito(id):
    habito_a_modificar = Habito.query.get(id)
    # Buscamos en la tabla de la base de datos el habito q tenga ese ID

    habito_a_modificar.completado = not habito_a_modificar.completado
    # Le cambiamos el estado de completacion al opuesto

    db.session.commit()
    # Guardamos los cambios en nuestro archivo de base de datos

    return redirect(url_for("inicio"))
    # url_for: direccion de web para "inicio"
    # redirect: redirecciona
    # Estás en la página principal (/) viendo tus hábitos.Haces clic en el botón y Chrome viaja hacia la ruta trasera de Flask (por ejemplo, /completar/1).
    # En esa ruta trasera, Python hace su magia: busca el hábito, le cambia el estado a Verdadero y lo guarda en la base de datos. ¡Pero esa ruta no tiene un archivo HTML o diseño visual para mostrarte!
    # Si nosotros no ponemos nada al final, la página se quedaría en blanco o daría error porque no sabe qué dibujarle al usuario.
    # Al poner return redirect(url_for("inicio")), le decimos: "Apenas termines de tachar y guardar el hábito en el Excel de fondo, agarrá al usuario y mandalo de regreso a la página principal a la velocidad de la luz".

@app.route("/eliminar/<int:id>")
def eliminar_habito(id):
    habito_a_eliminar = Habito.query.get(id)

    db.session.delete(habito_a_eliminar)

    db.session.commit()

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug = True)