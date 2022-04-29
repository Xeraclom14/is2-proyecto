from itertools import count
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import uuid

from __main__ import app
from __main__ import mysql

@app.route('/delete/<id>')
def delete(id):
    ## almacenar nombre
    cur = mysql.connection.cursor()
    cur.execute("SELECT titulo FROM encuesta WHERE id_encuesta = %s;",(id,))
    nombre = cur.fetchall()

    #encontrar todas las preguntas vinculadas a la encuesta
    cur.execute("SELECT * FROM pregunta WHERE id_encuesta = %s;",(id,))
    datos = cur.fetchall()

    for pregunta in datos:
        #borrar todas las respuestas y desarrollos vinculados a una pregunta
        cur.execute("DELETE FROM respuesta WHERE id_pregunta = %s;", (pregunta[0],))
        mysql.connection.commit()
        cur.execute("DELETE FROM desarrollo WHERE id_pregunta = %s;", (pregunta[0],))
        mysql.connection.commit()

    #eliminar todas las preguntas vinculadas a la encuesta
    cur.execute("DELETE FROM pregunta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()

    #eliminar la encuesta
    cur.execute("DELETE FROM encuesta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()
    flash("Encuesta \"" + nombre[0][0] +"\" eliminada exitosamente.")
    return redirect(url_for("forms"))