from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql

@app.route('/delete/<id>')
def delete(id):
    if 'loggedin' not in session:
        return(render_template("403.html"))

    if session['type'] == "encuestado":
        return(render_template("403.html"))

    cur = mysql.connection.cursor()

    # verificar si es una encuesta valida
    cur.execute("SELECT * FROM encuesta WHERE id_encuesta = %s AND id_encuestador = %s;",(id, session['id'],))
    validar = cur.fetchall()
    if validar == ():
        flash("danger","Se ha producido un error al intentar eliminar la encusta.")
        return redirect(url_for("forms"))

    # almacenar nombre
    cur.execute("SELECT titulo FROM encuesta WHERE id_encuesta = %s;",(id,))
    nombre = cur.fetchall()

    #encontrar todas las preguntas vinculadas a la encuesta
    cur.execute("SELECT * FROM pregunta WHERE id_encuesta = %s;",(id,))
    datos = cur.fetchall()

    for pregunta in datos:
        #borrar todas las respuestas y desarrollos vinculados a una pregunta
        cur.execute("DELETE FROM respuesta WHERE id_pregunta = %s;", (pregunta[0],))
        mysql.connection.commit()

        #No se haran respuestas de desarrollo por indicaciones del profesor
        #cur.execute("DELETE FROM desarrollo WHERE id_pregunta = %s;", (pregunta[0],))
        #mysql.connection.commit()

    #eliminar todas las preguntas vinculadas a la encuesta
    cur.execute("DELETE FROM pregunta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()

    #eliminar las referencias de categoria
    cur.execute("DELETE FROM encuestacategoria WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()

    #eliminar las referencias de encuestado_encuesta
    cur.execute("DELETE FROM encuestadoencuesta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()

    #eliminar la encuesta
    cur.execute("DELETE FROM encuesta WHERE id_encuesta = %s;", (id,))
    mysql.connection.commit()
    flash("success","Encuesta \"" + nombre[0][0] +"\" eliminada exitosamente.")

    return redirect(url_for("forms"))