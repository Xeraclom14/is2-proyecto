from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql

@app.route('/profile/<id>', methods=['GET','POST'])
def profile(id):
    if 'loggedin' not in session:
        return(render_template("403.html"))

    tiposesion = session['type']
    e_id = session['id']

    #"id" es un str, e_id es un int
    idint = int(id)

    #ya veremos
    if tiposesion == 'encuestador':
        return "Ya veremos."
    
    #Es un encuestado
    if tiposesion == 'encuestado':
        
        #es EL encuestado
        if idint == e_id:
            
            cur = mysql.connection.cursor()

            #Función para recibir las preferencias de una persona.
            cur.execute("SELECT DISTINCT categoria.id_categoria, categoria.nombre FROM categoria "
            + "JOIN encuestadocategoria on categoria.id_categoria = encuestadocategoria.id_categoria "
            + "AND encuestadocategoria.id_encuestado = %s "
            + "JOIN encuestado ON encuestado.id_encuestado = %s;",(id,id))
            
            datardos = cur.fetchall()
            categorias = []
            for categoria in datardos:
                categorias.append([categoria[0],categoria[1]])
            mysql.connection.commit()

            #Este apartado para hacer la función de agregar una preferencia a una persona.

            #Pero primero que nada, debo hacer otra que me de las NO preferencias de este.
            cur.execute("SELECT categoria.id_categoria, categoria.nombre "
            + "FROM categoria LEFT JOIN encuestadocategoria "
            + "ON (categoria.id_categoria = encuestadocategoria.id_categoria "
            + "AND encuestadocategoria.id_encuestado = %s) "
            + "WHERE encuestadocategoria.id_categoria IS NULL;",(id,))

            masdatardos = cur.fetchall()        
            nopreferidas = []
            for nopref in masdatardos:
                nopreferidas.append([nopref])
            mysql.connection.commit()

            #Función para recibir todas las encuestas contestadas
            cur.execute("SELECT encuesta.titulo FROM encuesta "
            + "INNER JOIN encuestadoencuesta "
            + "ON (encuesta.id_encuesta = encuestadoencuesta.id_encuesta "
            + "AND encuestadoencuesta.id_encuestado = %s);",(id,))

            datos = cur.fetchall()
            encuestas = []
            for encuesta in datos:
                encuestas.append([encuesta[0]])
            mysql.connection.commit()

            #Para los datos de la persona.
            dpers = []
            dpers.append(session['username'])
            dpers.append(session['username2'])
            dpers.append(session['ap1'])
            dpers.append(session['ap2'])
            dpers.append(session['mail'])

            id = idint;
            #Se ha seleccionado una preferencia a agregar
            #Y se ha hecho click en el botón de enviar.

            #quiero saber la preferencia de spam del encuestado.
            cur = mysql.connection.cursor()
            cur.execute("SELECT quierespam FROM encuestado WHERE id_encuestado = %s;",(id,))
            spam = cur.fetchone()
            mysql.connection.commit()

            return render_template("/encuestados/personal.html",
            dpers = dpers, forms = encuestas, categorias = categorias,
            nopreferidas = nopreferidas, id = id, spam = spam)

        #es un tercero
        else:
            return render_template("/403.html")
    
    return render_template("/403.html")

#Para que funcione el navbar.
@app.route('/profile', methods=['GET','POST'])
def profileinicio():

    if 'loggedin' not in session:
        return(render_template("403.html"))
    
    tiposesion = session['type']
    e_id = session['id']

    #Se ha optado por perfiles privados.
    if tiposesion == 'encuestador':
        return render_template("/encuestados/403.html")

    if tiposesion == 'encuestado':

        if request.method == 'POST':

                if (request.form['nuevapref'] != ""):
                    
                    idcat = request.form['nuevapref']

                    #regresar de inmediato si estás en "seleccionar categoria"
                    if(idcat == "0"):
                        print("pasa")
                        return redirect(url_for("profile", id=e_id ))

                    #si no, agregar categoria.
                    cur = mysql.connection.cursor()                
                    cur.execute("INSERT INTO encuestadocategoria VALUES (%s, %s);",(e_id, idcat))
                    mysql.connection.commit()

                    return redirect(url_for("profile", id=e_id ))

        return redirect(url_for("profile", id=e_id ))

    return render_template("/403.html")


@app.route('/delete_cat/<id>/<id_cat>')
def delete_cat(id,id_cat):
    tiposesion = session['type']
    e_id = str(session['id'])

    # verificar
    if tiposesion == 'encuestador':
        return render_template("/403.html")

    if tiposesion == 'encuestado':
        #Solamente la misma persona debe borrar.
        if id == e_id:

            #borrar la relación usuario-preferencia
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM encuestadocategoria "
            + "WHERE id_encuestado = %s AND id_categoria = %s;", (id,id_cat))
            mysql.connection.commit()
            #medio ambiente es "1"

            return redirect(url_for("profile", id=id ))

        return render_template("/403.html")
        

    return render_template("/403.html")

#ruta para editar preferencias
@app.route('/edit_sendmail/<id>')
def edit_sendmail(id):

    tiposesion = session['type']
    e_id = str(session['id'])

    # verificar
    if tiposesion == 'encuestador':
        return render_template("/403.html")

    if tiposesion == 'encuestado':
        #Solamente la misma persona debe editar.
        if id == e_id:
            
            #quiero el número.
            cur = mysql.connection.cursor()
            cur.execute("SELECT quierespam FROM encuestado WHERE id_encuestado = %s;",(id,))

            spam = cur.fetchone()
            mysql.connection.commit()

            #si el valor es 1, significa que NO quiere tener spam.
            if spam[0] == 1:
                cur = mysql.connection.cursor()
                cur.execute("UPDATE encuestado SET quierespam = 0 WHERE id_encuestado = %s;",(id,))
                mysql.connection.commit()
                return redirect(url_for("profile", id=id ))

            if spam[0] == 0:
                cur = mysql.connection.cursor()
                cur.execute("UPDATE encuestado SET quierespam = 1 WHERE id_encuestado = %s;",(id,))
                mysql.connection.commit()
                return redirect(url_for("profile", id=id ))

            return redirect(url_for("profile", id=id ))

        return render_template("/403.html")
