from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql

@app.route('/form/<id>', methods=['GET','POST'])
def form(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(titulo) FROM encuesta WHERE id_encuesta = " + id)
    ver = cur.fetchall()
    if(ver[0][0] == 0):
        flash("Encuesta no Encontrada.") 
        return redirect(url_for("forms"))
    #Inserción
    if request.method == 'POST':
        #if(request.form['algo'] != ""):
        #    cur = mysql.connection.cursor()
        #    cur.execute("INSERT INTO encuesta (id_encuestador, titulo) VALUES (%s , %s);", (e_id, request.form['titulo'],))
        #    mysql.connection.commit()
        #    flash("Encuesta \"" + request.form['titulo'] + "\" ingresada correctamente")
        #else:
        #    flash("Ingerese un valor valido")
        ### redirigir para borrar el formulario de la memoria (no se envia nuevamente si se recarga la pagina)
        return redirect(url_for("form"))

    #Visualización
    else:
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
        return render_template('/encuestadores/form.html', form = preguntas, titulo = nombre_encuesta[0][0])
