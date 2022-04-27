from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import uuid

from __main__ import app
from __main__ import mysql

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Correo insertado.
        if(request.form['correocito'] != ""):
            #conexión
            cur = mysql.connection.cursor() 
            #seleccionar cuenta
            cur.execute("SELECT prim_nom FROM encuestador WHERE email = %s AND password = %s;", (request.form['correocito'], request.form['passwordcita'],))
            #filtrar por una (no deberia ser necesario?)
            account = cur.fetchone()

            if account is None:
                flash("Usuario no encontrado")
                return redirect(url_for("login"))


            flash("Bienvenido, " + account[0][0] + "")
            return redirect(url_for("forms"))
        else:
            flash("Por favor, rellene los campos")
            return redirect(url_for("login"))
    else:
        return render_template('login.html')