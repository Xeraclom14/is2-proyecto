from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app
from __main__ import mysql
from __main__ import e_id

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        if(request.form['titulo'] != ""):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO encuesta (id_encuesta, id_encuestador, titulo) VALUES (1, %s , %s);", (e_id, request.form['titulo'],))
            mysql.connection.commit()

            ### TEXTO LIMPIO DE CATEGORIAS
            #categorias =  request.form['categoria'].upper().split(',')
            #for categoria in categorias:
            #    categoria = categoria.rstrip()
            #    categoria = categoria.lstrip()
            #    print(categoria)

            #print(request.form['titulo'])
            flash("Encuesta \"" + request.form['titulo'] + "\" ingresada correctamente")
            return redirect(url_for("forms"))
        else:
            print("Ingerese un valor valido")
        ### redirigir para borrar el formulario de la memoria (no se envia nuevamente si se recarga la pagina)
        return redirect(url_for("create"))
    else:
        return render_template('creation.html')