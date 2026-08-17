from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import date, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Habito(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    registros = db.relationship('Registro', backref = 'habito', lazy = True, cascade = "all, delete-orphan")

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date, default = date.today)
    habito_id = db.Column(db.Integer, db.ForeignKey('habito.id'), nullable = False)

with app.app_context():
    db.create_all()


# Ruta para la pagina principal
@app.route("/")
def inicio():
    lista_habitos = Habito.query.all()
    registros_hoy = Registro.query.filter_by(fecha = date.today()).all()
    ids_completados_hoy = [registro.habito_id for registro in registros_hoy]

    ultimos_7_dias = []

    for i in range(7):
        dia_calculado = date.today() - timedelta(days = i)
        ultimos_7_dias.append(dia_calculado)

    ultimos_7_dias.reverse()

    return render_template("index.html", 
                           habitos = lista_habitos,
                           completados_hoy = ids_completados_hoy,
                           fechas_semana = ultimos_7_dias)

# Ruta para agregar habitos
@app.route("/agregar", methods = ["POST"]) 
def agregar_habito():
    nombre_nuevo = request.form.get("nombre_habito")  
    nuevo_habito = Habito(nombre = nombre_nuevo)
    db.session.add(nuevo_habito)
    db.session.commit()  
    return redirect(url_for("inicio"))


# Ruta para marcar un habito como completado
@app.route("/completar/<int:id>")
def completar_habito(id):
    registro_hoy = Registro.query.filter_by(habito_id = id, fecha = date.today()).first()

    if registro_hoy:
        db.session.delete(registro_hoy)
    else:
        nuevo_registro = Registro(habito_id = id)
        db.session.add(nuevo_registro)

    db.session.commit()
    return redirect(url_for("inicio"))



# Ruta para eliminar un habito
@app.route("/eliminar/<int:id>")
def eliminar_habito(id):
    habito_a_eliminar = Habito.query.get(id)
    db.session.delete(habito_a_eliminar)
    db.session.commit()
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug = True)