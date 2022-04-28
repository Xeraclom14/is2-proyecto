from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import uuid

from __main__ import app
from __main__ import mysql

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Correo y contraseña insertados.
        if(request.form['correocito'] != "" and request.form['passwordcita'] != ""):
            
            #conexión
            cur = mysql.connection.cursor() 
            
            #seleccionar cuenta
            cur.execute("SELECT prim_nom, password FROM encuestador WHERE"
            +" email = %s AND password = %s;",
            (request.form['correocito'], request.form['passwordcita'],))
            
            #filtrar por una (no deberia ser necesario?)
            account = cur.fetchone()
            #print(account)

            #Si algún dato es incorrecto, sea nombre o contraseña.
            if account is None:
                flash("Datos Incorrectos")
                return redirect(url_for("login"))

            #No sirve.
            #if(request.form['passwordcita']!=account[1]):
            #    flash("Contraseña incorrecta")

            #Si fue exitoso.
            flash("Bienvenido, " + account[0])
            return redirect(url_for("forms"))
        
        #Si no ingresaste nada.
        else:
            flash("Por favor, rellene los campos")
            return redirect(url_for("login"))
    else:
        return render_template('login.html')