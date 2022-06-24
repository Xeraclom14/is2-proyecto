from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql

def verificar(id):
    if 'loggedin' not in session:
        return False
    if session['type'] == "encuestado":
        return False
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM encuesta WHERE id_encuesta = %s AND id_encuestador = %s;",(id, session['id'],))
    validar = cur.fetchall()
    if validar == ():
        return False
    return True

@app.route('/results/<id>', methods=['GET','POST'])
def results(id):
    #Verificar logeo
    if not verificar(id):
        flash("warning","Usted no puede ver los resultados de esta encuesta.")
        return redirect(url_for("forms"))

    cur = mysql.connection.cursor()
    #Form
    cur.execute("SELECT COUNT(titulo) FROM encuesta WHERE id_encuesta = " + id)
    ver = cur.fetchall()
    if(ver[0][0] == 0):
        flash("light","Encuesta no Encontrada.") 
        return redirect(url_for("forms"))

    #Encontrar el nombre de la encuesta en db
    cur.execute("SELECT titulo FROM encuesta WHERE id_encuesta = " + id)
    nombre_encuesta = cur.fetchall()
    
    #Retirar las preguntas asociadas a la encuesta
    cur.execute("SELECT * FROM pregunta WHERE id_encuesta = " + id)
    datos = cur.fetchall()
    #array con preguntas.
    preguntas = []
    
    #por cada pregunta...
    for pregunta in datos:
        cur.execute("SELECT * FROM respuesta WHERE id_pregunta  =%s;", (pregunta[0],))
        respuestas = cur.fetchall()
        nombres_respuestas = []
        cont_respuestas = []

        for respuesta in respuestas:
            nombres_respuestas.append(respuesta[2])
            cont_respuestas.append(respuesta[3])

        #esto recibiría el id_pregunta, id_encuesta, tipo, texto y respuestas.
        preguntas.append([pregunta[0], pregunta[1], pregunta[2], pregunta[4], nombres_respuestas, cont_respuestas])
    mysql.connection.commit()
    
    return render_template('/encuestadores/results.html', form = preguntas, titulo = nombre_encuesta[0][0], id = id)
