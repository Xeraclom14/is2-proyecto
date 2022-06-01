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

            #SELECT categoria.nombre FROM categoria 
            #JOIN encuestadocategoria ON categoria.id_categoria = encuestadocategoria.id_categoria
            #AND encuestadocategoria.id_encuestado = 1
            #JOIN encuestado ON encuestado.id_encuestado = 1;

            #Función para agregarle una preferencia a una persona.

            #cur.execute("INSERT INTO encuestadoencuesta "
            #+ "VALUES %s, %s ",(id,"algo"))
            #mysql.connection.commit()

            

            #Función para recibir todas las encuestas contestadas
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
            nombre = session['username'], forms = encuestas, categorias = categorias)

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