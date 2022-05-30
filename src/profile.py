from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app
from __main__ import mysql

@app.route('/profile/<id>', methods=['GET','POST'])
def profile(id):
    if 'loggedin' not in session:
        return(render_template("403.html"))

    tiposesion = session['type']
    e_id = session['id']

    #"id" es un str, e_id es un int
    idint = int(id)

    #ya veremo
    if tiposesion == 'encuestador':
        return "Ya veremos."
    
    #Es un encuestado
    if tiposesion == 'encuestado':
        
        #es EL encuestado
        if idint == e_id:
            

            #Función para recibir todas las encuestas contestadas
            cur = mysql.connection.cursor()

            #que mal.
            #Distinct me permite evitar duplicados, pero algo está mal, porque no debería usarlo.
            cur.execute("SELECT DISTINCT encuesta.titulo, encuestado.prim_nom FROM encuesta "
            + "JOIN encuestadoencuesta ON encuesta.id_encuesta = encuestadoencuesta.id_encuesta "
            + "JOIN encuestado ON encuestado.id_encuestado = %s;",(id))
            datos = cur.fetchall()
            encuestas = []
            for encuesta in datos:
                encuestas.append([encuesta[0]])
            mysql.connection.commit()

            return render_template("/encuestados/personal.html",
            nombre = session['username'], forms = encuestas)

        #es un tercero
        else:
            return render_template("/encuestados/tercero.html")
    
    return render_template("/encuestados/403.html")
    

#Para que funcione el navbar.
@app.route('/profile', methods=['GET','POST'])
def profileinicio():

    if 'loggedin' not in session:
        return(render_template("403.html"))
    
    tiposesion = session['type']
    e_id = session['id']

    #ya veremo
    if tiposesion == 'encuestador':
        return "Ya veremos."

    if tiposesion == 'encuestado':
        return redirect(url_for("profile", id=e_id ))

    return render_template("/encuestados/403.html")