from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql

@app.route('/login', methods=['GET', 'POST'])
def login():
    #extrae los argumentos de id_encuesta para redirigir (de ser necesario)
    id_encuesta = request.args.get('id_encuesta')

    #por qué irías a logearte, si ya hay una cuenta?
    if 'loggedin' in session:
        return(render_template("403.html"))

    if request.method == 'POST':
        #Correo y contraseña insertados.
        if(request.form['correocito'] != "" and request.form['passwordcita'] != ""):
            
            #conexión
            cur = mysql.connection.cursor() 
            
            #seleccionar cuenta
            cur.execute("SELECT * FROM encuestado WHERE"
            +" email = %s AND password = %s;",
            (request.form['correocito'], request.form['passwordcita'],))

            #ORDEN: ID, Ap1, Ap2, No1, No2, mail, pass
            
            #filtrar por una (no deberia ser necesario?)
            account = cur.fetchone()

            #Si algún dato es incorrecto, sea nombre o contraseña.
            if account is None:
                flash("Datos Incorrectos")
                if id_encuesta != None:
                    return redirect(url_for("login", id_encuesta = id_encuesta))
                return redirect(url_for("login"))
                    

            #No sirve.
            #if(request.form['passwordcita']!=account[1]):
            #    flash("Contraseña incorrecta")

            #Si fue exitoso...
            if account:
                flash("Bienvenido, " + account[3])
                    
            #ORDEN: ID, Ap1, Ap2, No1, No2, mail, pass

                #cosas de flask
                session['loggedin'] = True
                session['username'] = account[3]
                session['password'] = account[6]
                session['mail'] = account[5]
                session['type'] = "encuestado"
                session['id'] = account[0]
                session['ap1'] = account[1]
                session['ap2'] = account[2]
                session['username2'] = account[4]
                if id_encuesta != None:
                    return redirect("form/" + id_encuesta)
                return redirect(url_for("Index")) #se usa ident???????????????
        
        #Si no ingresaste nada.
        else:
            flash("Por favor, rellene los campos")
            if id_encuesta != None:
                return redirect(url_for("login", id_encuesta = id_encuesta))
            return redirect(url_for("login"))
    else:
        return render_template('login.html', id_encuesta = id_encuesta)