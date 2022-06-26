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

    #Si la encuesta esta cerrada, no se debe poder editar.
    cur.execute("SELECT cerrada FROM encuesta WHERE id_encuesta = " + id)
    validar = cur.fetchall()
    mysql.connection.commit()

    if(validar[0][0] == 1):
        return False
    return True

@app.route('/required/<id>/<id_pregunta>/<bool_pregunta>')
def required(id, id_pregunta, bool_pregunta):
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))
    cur = mysql.connection.cursor()
    print(bool_pregunta)
    if bool_pregunta == '1':
        cur.execute("UPDATE pregunta SET obligatoria = %s WHERE id_pregunta = %s;", (0, id_pregunta,))
    else:
        cur.execute("UPDATE pregunta SET obligatoria = %s WHERE id_pregunta = %s;", (1, id_pregunta,))
    mysql.connection.commit()
    flash("success","Pregunta actualizada.")
    return redirect("/edit/" + id)

@app.route('/edit_respuesta/<id>/<id_pregunta>/<id_respuesta>', methods=['GET','POST'])
def edit_respuesta(id,id_pregunta,id_respuesta):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))
    # editar respuesta
    if request.method == 'POST':
        if(request.form['respuesta']!=""):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE respuesta SET texto_respuesta = %s WHERE respuesta.id_respuesta = %s;", (request.form['respuesta'],id_respuesta,))
            mysql.connection.commit()
            flash("success","Pregunta actualizada.")
            return redirect("/edit/" + id)
        else:
            flash("warning","Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)

@app.route('/edit_pregunta/<id>/<id_pregunta>', methods=['GET','POST'])
def edit_pregunta(id,id_pregunta):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))
    #editar pregunta
    if request.method == 'POST':
        if(request.form['pregunta']!=""):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE pregunta SET texto_pregunta = %s WHERE pregunta.id_pregunta = %s;", (request.form['pregunta'],id_pregunta,))
            mysql.connection.commit()
            flash("success","Pregunta actualizada.")
            return redirect("/edit/" + id)
        else:
            flash("warning","Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)

@app.route('/edit_titulo/<id>', methods=['GET','POST'])
def edit_titulo(id):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))
    # editar titulo
    if request.method == 'POST':
        if(request.form['titulo']!=""):
            cur = mysql.connection.cursor()
            cur.execute("UPDATE encuesta SET titulo = %s WHERE encuesta.id_encuesta = %s;", (request.form['titulo'],id,))
            mysql.connection.commit()
            flash("success","Título actualizado.")
            return redirect("/edit/" + id)
        else:
            flash("warning","Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)

@app.route('/add_categoria/<id>', methods=['GET', 'POST'])
def add_categoria(id):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))

    #agregar categoria
    if request.method == 'POST':
        if(request.form['categoria']!=""):
            cur = mysql.connection.cursor()
            cur.execute("SELECT nombre FROM categoria WHERE nombre = %s", (request.form['categoria'],))
            existe = cur.fetchall()

            if(len(existe) == 0): #en caso de que la categoria no se encuentra en la DB, se crea
                cur.execute("INSERT INTO categoria (nombre, descripcion) VALUES (%s , %s);", (request.form['categoria'], request.form['categoria']))

            #verificar si ya se agrego la categoria anteriormente
            cur.execute("SELECT id_categoria FROM categoria WHERE nombre = %s", (request.form['categoria'],))
            id_cat = cur.fetchall()[0][0]

            cur.execute("SELECT * FROM encuestacategoria WHERE id_encuesta = %s AND id_categoria = %s", (id, id_cat))
            existe = cur.fetchall()
            if(len(existe) > 0): #en caso de que la categoria ya se haya agregado anteriormente
                flash("warning","La encuesta ya tiene esta categoria.")
                mysql.connection.commit()
                return redirect("/edit/" + id)
                
            #linkear la encuesta con la categoria
            cur.execute("INSERT INTO encuestacategoria (id_encuesta, id_categoria) VALUES (%s , %s);", (id, id_cat))

            mysql.connection.commit()

            flash("success","Categoria agregada.")

            return redirect(request.referrer)
        else:
            flash("warning","Ingerese un valor valido.")
            return redirect("/edit/" + id)

    return redirect("/edit/" + id)

@app.route('/remove_categoria/<id>/<id_cat>', methods=['GET', 'POST'])
def remove_categoria(id, id_cat):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))


    #remover categoria
    if request.method == 'POST':
        
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM encuestacategoria WHERE id_encuesta = %s AND id_categoria = %s;", (id,id_cat))
        mysql.connection.commit()

        flash("success","Categoria removida.")
        return redirect(request.referrer)

    return redirect("/edit/" + id)

@app.route('/new_alternativa/<id>/<id_pregunta>', methods=['GET','POST'])
def new_alternativa(id,id_pregunta):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))

    #agregar alternativa
    if request.method == 'POST':
        if(request.form['alternativa']!=""):
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO respuesta (id_pregunta, texto_respuesta) VALUES (%s , %s);", (id_pregunta ,request.form['alternativa'],))
            mysql.connection.commit()
            return redirect(request.referrer)
        else:
            flash("warning","Ingerese un valor valido.")
            return redirect("/edit/" + id)
    return redirect("/edit/" + id)

@app.route('/delete_alternativa/<id>/<id_alternativa>')
def delete_alternativa(id,id_alternativa):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))

    #borrar la respuesta
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM respuesta WHERE id_respuesta = %s;", (id_alternativa,))
    mysql.connection.commit()
    flash("success","Respuesta eliminada.")
    return redirect("/edit/" + id)

@app.route('/delete_pregunta/<id>/<id_pregunta>')
def delete_pregunta(id,id_pregunta):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))

    #borrar todas las respuestas vinculados a la pregunta
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM respuesta WHERE id_pregunta = %s;", (id_pregunta,))
    mysql.connection.commit()
    
    #eliminar la pregunta
    cur.execute("DELETE FROM pregunta WHERE id_pregunta = %s;", (id_pregunta,))
    mysql.connection.commit()
    flash("success","Pregunta eliminada.")
    return redirect("/edit/" + id)

@app.route('/edit/<id>', methods=['GET','POST'])
def edit(id):
    cur = mysql.connection.cursor()
    #Prohibido acceder a personas que no están registradas.
    if 'loggedin' not in session:
        return(render_template("403.html"))

    tiposesion = session['type']

    #Los encuestados tampoco deberían editar las encuestas.
    if(tiposesion == "encuestado"):
        return(render_template("403.html"))

    # verificar
    if not verificar(id):
        flash("warning","Usted no puede editar esta encuesta.")
        return redirect(url_for("forms"))

    #edit
    if request.method == 'POST':
        if(request.form['pregunta'] != ""):
            tipo_pregunta = -1
            if request.form.get('D'):
                tipo_pregunta = 0
            elif  request.form.get('S'):
                tipo_pregunta = 2
            else :
                tipo_pregunta = 1
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO pregunta (id_encuesta, tipo_pregunta ,texto_pregunta) VALUES (%s , %s, %s);", (id , tipo_pregunta ,request.form['pregunta'],))
            mysql.connection.commit()
            flash("success","Pregunta ingresada correctamente.")
        else:
            flash("warning","Ingerese un valor valido.")
        return redirect(request.referrer) #refresh

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
            #esto recibiría el id_pregunta, id_encuesta, respuestas, tipo y el texto y obligatoria
            preguntas.append([pregunta[0], pregunta[1], respuestas, pregunta[2], pregunta[4], pregunta[3]])

        #retirar categorias asociadas a la encuesta
        cur.execute("SELECT categoria.id_categoria, nombre FROM categoria, encuestacategoria "
         + "WHERE categoria.id_categoria = encuestacategoria.id_categoria AND encuestacategoria.id_encuesta = " + id)
        categorias = cur.fetchall()
        
        mysql.connection.commit()
        return render_template('/encuestadores/edit.html', form = preguntas, titulo = nombre_encuesta[0][0], id = id, categorias = categorias)

@app.route('/cerrar_encuesta/<id>', methods=['GET','POST'])
def cerrar_encuesta(id):
    # verificar
    if not verificar(id):
        flash("warning","Usted no puede Cerrar esta encuesta.")
        return redirect(url_for("forms"))

    # Nombre de la encuesta
    cur = mysql.connection.cursor()
    cur.execute("SELECT titulo FROM encuesta WHERE id_encuesta = " + id)
    nombre_encuesta = cur.fetchall()

    #Retirar las preguntas asociadas a la encuesta

    cur.execute("SELECT * FROM pregunta WHERE id_encuesta = " + id)
    datos = cur.fetchall()

    #Checkear si la encuesta contiene preguntas
    if len(datos) == 0:
        flash("danger","Error: La encuesta no contiene preguntas.")
        mysql.connection.commit()
        return redirect(request.referrer) #refresh

    #Por cada pregunta...
    for pregunta in datos:
        cur.execute("SELECT * FROM respuesta WHERE id_pregunta  =%s;", (pregunta[0],))
        respuestas = cur.fetchall()

        #Para preguntas de alternativas o s.multiple, se necesitan almenos 2 respuestas
        if pregunta[2] != 0 and len(respuestas) < 2:
            flash("warning","Error: La pregunta '" + pregunta[4] + "' debe contener almenos 2 respuestas.")
            mysql.connection.commit()
            return redirect(request.referrer) #refresh

    #En caso de no haber fallo, cerramos la encuesta
    cur.execute("UPDATE encuesta SET cerrada = '1' WHERE encuesta.id_encuesta = " + id)
    mysql.connection.commit()

    flash("success","Se ha cerrado la encuesta '" + nombre_encuesta[0][0] + "'.")

    return redirect("/forms")