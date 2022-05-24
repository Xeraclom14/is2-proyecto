import string
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql, e_id

@app.route('/edit_respuesta/<id>/<id_pregunta>/<id_respuesta>', methods=['GET','POST'])
def edit_respuesta(id,id_pregunta,id_respuesta):
    if request.method == 'POST':
        if(request.form['respuesta']!=""):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE respuesta SET texto_respuesta = %s WHERE respuesta.id_respuesta = %s;", (request.form['respuesta'],id_respuesta,))
            mysql.connection.commit()
            flash("Pregunta actualizada.")
            return redirect("/edit/" + id)
        else:
            flash("Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)

@app.route('/edit_pregunta/<id>/<id_pregunta>', methods=['GET','POST'])
def edit_pregunta(id,id_pregunta):
    if request.method == 'POST':
        if(request.form['pregunta']!=""):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE pregunta SET texto_pregunta = %s WHERE pregunta.id_pregunta = %s;", (request.form['pregunta'],id_pregunta,))
            mysql.connection.commit()
            flash("Pregunta actualizada.")
            return redirect("/edit/" + id)
        else:
            flash("Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)

@app.route('/edit_titulo/<id>', methods=['GET','POST'])
def edit_titulo(id):
    if request.method == 'POST':
        if(request.form['titulo']!=""):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE encuesta SET titulo = %s WHERE encuesta.id_encuesta = %s;", (request.form['titulo'],id,))
            mysql.connection.commit()
            flash("Título actualizado.")
            return redirect("/edit/" + id)
        else:
            flash("Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)


@app.route('/new_alternativa/<id>/<id_pregunta>', methods=['GET','POST'])
def new_alternativa(id,id_pregunta):
    if request.method == 'POST':
        if(request.form['alternativa']!=""):
            print(request.form['alternativa'])
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO respuesta (id_pregunta, texto_respuesta) VALUES (%s , %s);", (id_pregunta ,request.form['alternativa'],))
            mysql.connection.commit()
            return redirect(request.referrer)
        else:
            flash("Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)

@app.route('/delete_alternativa/<id>/<id_alternativa>')
def delete_alternativa(id,id_alternativa):
    cur = mysql.connection.cursor()
    
    #borrar la respuesta
    cur.execute("DELETE FROM respuesta WHERE id_respuesta = %s;", (id_alternativa,))
    mysql.connection.commit()
    flash("Respuesta eliminada.")
    return redirect("/edit/" + id)

@app.route('/delete_pregunta/<id>/<id_pregunta>')
def delete_pregunta(id,id_pregunta):
    cur = mysql.connection.cursor()

    #borrar todas las respuestas vinculados a la pregunta
    cur.execute("DELETE FROM respuesta WHERE id_pregunta = %s;", (id_pregunta,))
    mysql.connection.commit()
    
    #eliminar la pregunta
    cur.execute("DELETE FROM pregunta WHERE id_pregunta = %s;", (id_pregunta,))
    mysql.connection.commit()
    flash("Pregunta eliminada.")
    return redirect("/edit/" + id)

@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):

    #Prohibido acceder a personas que no están registradas.
    if 'loggedin' not in session:
        return(render_template("403.html"))

    tiposesion = session['type']

    #Los encuestados tampoco deberían editar las encuestas.
    if(tiposesion == "encuestado"):
        return(render_template("403.html"))

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
        return render_template('/encuestadores/edit.html', form = preguntas, titulo = nombre_encuesta[0][0], id = id)

@app.route('/cerrar_encuesta/<id>', methods=['GET','POST'])
def cerrar_encuesta(id):
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE encuesta SET cerrada = '1' WHERE encuesta.id_encuesta = " + id)

    cur.execute("SELECT titulo FROM encuesta WHERE id_encuesta = " + id)
    nombre_encuesta = cur.fetchall()

    mysql.connection.commit()
    flash("Se ha cerrado la encuesta " + nombre_encuesta[0][0] + ".")

    return redirect("/forms")