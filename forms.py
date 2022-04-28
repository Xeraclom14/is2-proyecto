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
            cur.execute("INSERT INTO encuesta (id_encuestador, titulo) VALUES (%s , %s);", (e_id, request.form['titulo'],))
            mysql.connection.commit()
            flash("Encuesta \"" + request.form['titulo'] + "\" ingresada correctamente")
        else:
            flash("Ingerese un valor valido")
        ### redirigir para borrar el formulario de la memoria (no se envia nuevamente si se recarga la pagina)
        return redirect(url_for("forms"))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM encuesta")
        datos = cur.fetchall()
        mysql.connection.commit()
        return render_template('forms.html', forms = datos)