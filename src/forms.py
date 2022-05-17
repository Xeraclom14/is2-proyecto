from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app
from __main__ import mysql
from __main__ import e_id

@app.route('/forms', methods=['GET','POST'])
def forms():
    if request.method == 'POST':
        if(request.form['titulo'] != ""):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO encuesta (id_encuestador, titulo, cerrada) VALUES (%s , %s, 0);", (e_id, request.form['titulo'],))
            mysql.connection.commit()
            flash("Encuesta \"" + request.form['titulo'] + "\" ingresada correctamente.")
        else:
            flash("Ingerese un valor valido.")
        ### redirigir para borrar el formulario de la memoria (no se envia nuevamente si se recarga la pagina)
        return redirect(request.referrer)
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM encuesta ORDER BY fecha DESC;")
        datos = cur.fetchall()
        encuestas = []
        for encuesta in datos:
            cur.execute("SELECT COUNT(id_pregunta) From pregunta WHERE id_Encuesta =%s;", (encuesta[0],))
            num_preguntas = cur.fetchall()
            cur.execute("SELECT COUNT(id_encuesta) From encuestadoencuesta WHERE id_Encuesta =%s;", (encuesta[0],))
            num_respuestas = cur.fetchall()
            encuestas.append([encuesta[0], num_preguntas[0][0], encuesta[2], encuesta[3], num_respuestas[0][0], encuesta[4]])
        mysql.connection.commit()
        return render_template('encuestadores/forms.html', forms = encuestas)