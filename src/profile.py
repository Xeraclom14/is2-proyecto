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

    #ya veremo
    if tiposesion == 'encuestador':
        return "Ya veremos."
    
    #Es un encuestado
    if tiposesion == 'encuestado':
        
        #es EL encuestado
        if idint == e_id:
            
            cur = mysql.connection.cursor()

            #Función para recibir las preferencias de una persona.
            cur.execute("SELECT DISTINCT categoria.nombre FROM categoria "
            + "JOIN encuestadocategoria on categoria.id_categoria = encuestadocategoria.id_categoria "
            + "AND encuestadocategoria.id_encuestado = %s"
            + "JOIN encuestado ON encuestado.id_encuestado = %s",(id,id))
            
            datardos = cur.fetchall()
            categorias = []
            for categoria in datardos:
                categorias.append([categoria[0]])
            mysql.connection.commit()

            #Este apartado para hacer la función de agregar una preferencia a una persona.

            #SELECT DISTINCT categoria.* FROM categoria, encuestado
            #WHERE categoria.id_categoria NOT IN
            #(SELECT encuestadocategoria.id_categoria FROM encuestadocategoria, encuestado
            #WHERE encuestadocategoria.id_encuestado = encuestado.id_encuestado 
            #AND encuestado.id_encuestado = 1)

            #Pero primero que nada, debo hacer otra que me de las NO preferencias de este.
            cur.execute("SELECT DISTINCT categoria.* FROM categoria, encuestado "
            + "WHERE categoria.id_categoria NOT IN "
            + "(SELECT encuestadocategoria.id_categoria FROM encuestadocategoria, encuestado "
            + "WHERE encuestadocategoria.id_encuestado = encuestado.id_encuestado "
            + "AND encuestado.id_encuestado = %s);",(id))

            masdatardos = cur.fetchall()
            nopreferidas = []
            for nopref in masdatardos:
                nopreferidas.append([nopref])
            mysql.connection.commit()

            #Ahora debo hacer una consulta pa sacar el resultado seleccionado.
            #cur.execute("SELECT id_categoria FROM categoria WHERE nombre = %s",("algo"))

            #cur.execute("INSERT INTO encuestadocategoria "
            #+ "VALUES %s, %s ",(id,"numerocategoria"))
            #mysql.connection.commit()
            
            #Función para recibir todas las encuestas contestadas
            #que mal.
            #Distinct me permite evitar duplicados, pero algo está mal, porque no debería usarlo.
            #Puede estar mala.
            cur.execute("SELECT DISTINCT encuesta.titulo, encuestado.prim_nom FROM encuesta "
            + "JOIN encuestadoencuesta ON encuesta.id_encuesta = encuestadoencuesta.id_encuesta "
            + "JOIN encuestado ON encuestado.id_encuestado = %s;",(id))
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

            #Se ha seleccionado una preferencia a agregar
            #Y se ha hecho click en el botón de enviar.

            return render_template("/encuestados/personal.html",
            dpers = dpers, forms = encuestas, categorias = categorias,
            nopreferidas = nopreferidas)

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

        if request.method == 'POST':

                if (request.form['nuevapref'] != ""):
                    
                    idcat = request.form['nuevapref']

                    #regresar de inmediato si estás en "seleccionar categoria"
                    if(idcat == 0): return redirect(url_for("profile", id=e_id ))

                    #si no, agregar categoria.
                    cur = mysql.connection.cursor()                
                    cur.execute("INSERT INTO encuestadocategoria VALUES (%s, %s);",(e_id, idcat))
                    mysql.connection.commit()

                    return redirect(url_for("profile", id=e_id ))

        return redirect(url_for("profile", id=e_id ))

    return render_template("/encuestados/403.html")