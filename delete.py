from itertools import count
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import uuid

from __main__ import app
from __main__ import mysql

@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT titulo FROM encuesta WHERE id_encuesta = %s;",(id,))
    datos = cur.fetchall()
    cur.execute("DELETE FROM pregunta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()
    cur.execute("DELETE FROM encuesta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()
    flash("Encuesta \"" + datos[0][0] +"\" eliminada exitosamente.")
    return redirect(url_for("forms"))