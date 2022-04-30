import string
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app
from __main__ import mysql
from __main__ import e_id

@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        if(request.form['pregunta'] != ""):
            tipo_pregunta = -1;
            if request.form.get('D'):
                tipo_pregunta = 0
            elif  request.form.get('S'):
                tipo_pregunta = 2
            else :
                tipo_pregunta = 1
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO pregunta (id_encuesta, tipo_pregunta ,texto_pregunta) VALUES (%s , %s, %s);", (id , tipo_pregunta ,request.form['pregunta'],))
            mysql.connection.commit()
            flash("Pregunta ingresada correctamente.")
        else:
            flash("Ingerese un valor valido.")
        return redirect(request.referrer) #refresh

    #Visualización
    else:
        cur = mysql.connection.cursor()

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
            #Valores de Pregunta:
            # [0] = id_pregunta
            # [1] = id_encuesta 
            # [2] = tipo_pregunta
            # [3] = obligatoria
            # [4] = texto_pregunta
            #esto recibiría el id_pregunta, id_encuesta, respuestas, tipo y el texto.
            preguntas.append([pregunta[0], pregunta[1], respuestas, pregunta[2], pregunta[4]])
        mysql.connection.commit()
        return render_template('edit.html', form = preguntas, titulo = nombre_encuesta[0][0], id = id)
