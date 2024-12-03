from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secretos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Secreto
class Secreto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.String(255), nullable=False)
    likes = db.Column(db.Integer, default=0)
    loves = db.Column(db.Integer, default=0)
    categoria = db.Column(db.String(100))
    aprobado = db.Column(db.Boolean, default=False)  # Para la moderación de secretos

    def __repr__(self):
        return f'<Secreto {self.id} - {self.contenido}>'

# Ruta principal: muestra todos los secretos
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        contenido = request.form["contenido"]
        categoria = request.form["categoria"]
        nuevo_secreto = Secreto(contenido=contenido, categoria=categoria)
        db.session.add(nuevo_secreto)
        db.session.commit()
        return redirect(url_for("index"))

    # Lógica de búsqueda de secretos
    search_query = request.args.get('search', '')
    if search_query:
        secretos = Secreto.query.filter(Secreto.contenido.like(f'%{search_query}%')).all()
    else:
        secretos = Secreto.query.order_by(Secreto.id.desc()).all()

    return render_template("index.html", secretos=secretos)

# Ruta para dar like a un secreto
@app.route("/like/<int:id>")
def like_secreto(id):
    secreto = Secreto.query.get_or_404(id)
    secreto.likes += 1
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para dar love a un secreto
@app.route("/love/<int:id>")
def love_secreto(id):
    secreto = Secreto.query.get_or_404(id)
    secreto.loves += 1
    db.session.commit()
    return redirect(url_for('index'))

# Ruta para aprobar un secreto (solo para administradores)
@app.route("/aprobar/<int:id>")
def aprobar_secreto(id):
    secreto = Secreto.query.get_or_404(id)
    secreto.aprobado = True
    db.session.commit()
    return redirect(url_for("index"))

# Ruta para ver los secretos más populares (por likes)
@app.route("/populares")
def populares():
    secretos = Secreto.query.order_by(Secreto.likes.desc()).limit(5).all()
    return render_template("index.html", secretos=secretos)

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)