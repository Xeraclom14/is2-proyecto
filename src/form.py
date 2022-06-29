from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

from __main__ import app, mysql, mail

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

@app.route('/form/<id>', methods=['GET','POST'])
def form(id):
    cur = mysql.connection.cursor()
    #Verificar logeo
    if 'loggedin' not in session:
        flash("secondary","Por Favor, inicie sesión antes de contestar")
        return redirect(url_for("login", id_encuesta = id))

    #Form
    cur.execute("SELECT COUNT(titulo) FROM encuesta WHERE id_encuesta = " + id)
    ver = cur.fetchall()
    if(ver[0][0] == 0):
        flash("light","Encuesta no Encontrada.") 
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
        if session['type'] == "encuestado":
            return render_template('/encuestados/form.html', form = preguntas, titulo = nombre_encuesta[0][0], id = id)
        else:
            return render_template('/encuestadores/form.html', form = preguntas, titulo = nombre_encuesta[0][0], id = id)

@app.route('/enviar_encuesta/<id>', methods=['GET','POST'])
def enviar_encuesta(id):
    # verificar

    if not verificar(id):
        flash("warning","Usted no puede enviar esta encuesta.")
        return redirect(url_for("forms"))

    # Verificar que la encuesta esta cerrada
    cur = mysql.connection.cursor()
    cur.execute("SELECT cerrada FROM encuesta WHERE id_encuesta = " + id)
    cerrada = cur.fetchall()
    if cerrada[0][0] < 1:
        flash("danger","Error: La encuesta no esta cerrada")
        mysql.connection.commit()
        return redirect(request.referrer) #refresh

    # Retirar las categorias asociadas a la encuesta
    cur.execute("SELECT id_categoria FROM encuestacategoria WHERE id_encuesta = " + id)
    categorias = cur.fetchall()

    # Retirar encuestados cuya preferencia coincide con alguna categoria

    encuestados = []

    for categoria in categorias:
        cur.execute("SELECT email, prim_nom FROM encuestado, encuestadocategoria WHERE encuestado.id_encuestado = encuestadocategoria.id_encuestado AND encuestadocategoria.id_categoria = " + str(categoria[0]))
        resultados = cur.fetchall()
        for encuestado in resultados:
            encuestados.append(encuestado)
    
    mysql.connection.commit()

    # Eliminar encuestados duplicados (al coincidir con mas de 1 categoria)
    encuestados = list(dict.fromkeys(encuestados))

    # Queda registrado en la consola a quien se envio la encuesta.
    print(encuestados)

    with mail.connect() as conn:
        for encuestado in encuestados:
            message = 'Has sido seleccionado para contestar una encuesta: https://is2-2022.inf.udec.cl:5008/form/'+id
            subject = "Hola, %s" % encuestado[1]
            msg = Message(recipients=[encuestado[0]],
                        body=message,
                        subject=subject)
    
            conn.send(msg)

    return redirect("/forms")
    
# Guardar respuesta subir
# Marcar como contestado
@app.route('/submit_respuestas/<id>', methods=['GET','POST'])
def submit_respuestas(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pregunta WHERE id_encuesta = " + id)
    datos = cur.fetchall()

    #cur.execute("UPDATE respuesta SET contador_de_respuesta = 0")
    #mysql.connection.commit()

    for dato in datos:
        alts = request.form.getlist(str(dato[0]))
        for alt in alts:
            cur.execute("UPDATE respuesta SET contador_de_respuesta = contador_de_respuesta + 1 WHERE id_respuesta = %s", (alt,))
            mysql.connection.commit()
    
    cur.execute("INSERT INTO encuestadoencuesta VALUES (%s, %s)", (session['id'],id))
    mysql.connection.commit()

    return redirect("/forms")
