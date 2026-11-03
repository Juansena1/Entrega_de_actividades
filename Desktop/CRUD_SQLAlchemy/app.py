

import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "cambia-esta-clave-en-produccion")

# Cambia DB_PASSWORD por la contraseña de tu usuario MySQL.
# También puedes definir las variables DB_USER, DB_PASSWORD, DB_HOST y DB_NAME
# en las variables de entorno de Windows.
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "flask_sqlalchemy")

# quote_plus permite usar caracteres especiales en la contraseña.
from urllib.parse import quote_plus
password = quote_plus(DB_PASSWORD)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(30), nullable=True)

    def __repr__(self):
        return f"<Person {self.name}>"


@app.route("/")
def index():
    people = Person.query.order_by(Person.id.desc()).all()
    return render_template("index.html", people=people)


@app.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        if not name or not email:
            flash("El nombre y el correo son obligatorios.", "error")
            return render_template("crear.html")

        person = Person(name=name, email=email, phone=phone or None)
        db.session.add(person)

        try:
            db.session.commit()
            flash("Persona registrada correctamente.", "success")
            return redirect(url_for("index"))
        except IntegrityError:
            db.session.rollback()
            flash("Ya existe una persona registrada con ese correo.", "error")

    return render_template("crear.html")


@app.route("/editar/<int:person_id>", methods=["GET", "POST"])
def editar(person_id):
    person = db.get_or_404(Person, person_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        if not name or not email:
            flash("El nombre y el correo son obligatorios.", "error")
            return render_template("editar.html", person=person)

        person.name = name
        person.email = email
        person.phone = phone or None

        try:
            db.session.commit()
            flash("Persona actualizada correctamente.", "success")
            return redirect(url_for("index"))
        except IntegrityError:
            db.session.rollback()
            flash("Ese correo ya está asociado a otra persona.", "error")

    return render_template("editar.html", person=person)


@app.route("/eliminar/<int:person_id>", methods=["POST"])
def eliminar(person_id):
    person = db.get_or_404(Person, person_id)
    db.session.delete(person)
    db.session.commit()
    flash("Persona eliminada correctamente.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
