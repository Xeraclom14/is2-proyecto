from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql

@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():

    #por qué irías a logearte, si ya hay una cuenta?
    if 'loggedin' in session:
        return(render_template("403.html"))

    if request.method == 'POST':
        #Correo y contraseña insertados.
        if(request.form['correocito'] != "" and request.form['passwordcita'] != ""):
            
            #conexión
            cur = mysql.connection.cursor() 
            
            #seleccionar cuenta
            cur.execute("SELECT * FROM encuestador WHERE"
            +" email = %s AND password = %s;",
            (request.form['correocito'], request.form['passwordcita'],))

            #ORDEN: ID, Ap1, Ap2, No1, No2, mail, pass
            
            #filtrar por una (no deberia ser necesario?)
            account = cur.fetchone()

            #Si algún dato es incorrecto, sea nombre o contraseña.
            if account is None:
                flash("Datos Incorrectos")
                return redirect(url_for("loginadmin"))

            #No sirve.
            #if(request.form['passwordcita']!=account[1]):
            #    flash("Contraseña incorrecta")

            #Si fue exitoso...
            if account:
                flash("Bienvenido, " + account[3])
                
                #cosas de flask
                session['loggedin'] = True
                session['username'] = account[3]
                session['password'] = account[6]
                session['mail'] = account[5]
                session['type'] = "encuestador"
                session['id'] = account[0]

                return redirect(url_for("forms"))
        
        #Si no ingresaste nada.
        else:
            flash("Por favor, rellene los campos")
            return redirect(url_for("loginadmin"))
    else:
        return render_template('loginadmin.html')