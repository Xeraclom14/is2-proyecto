from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import uuid

from __main__ import app
from __main__ import mysql

@app.route('/register', methods=['GET', 'POST'])
def register():

   #por qué te registrarías, si ya hay una cuenta?
    if 'loggedin' in session:
        return(render_template("403.html"))

    if request.method == 'POST': 
       
       #Correo y contraseña insertados.
       if(request.form['prim_nom'] != "" and request.form['seg_nom'] != "" and request.form['ap_pat'] != "" and request.form['ap_mat'] != "" and request.form['email'] != "" and request.form['password'] != ""):
       
            nombre = request.form['prim_nom']
            nombre2 = request.form['seg_nom']
            apellido = request.form['ap_pat']
            apellido2 = request.form['ap_mat']
            email = request.form['email']
            password = request.form['password']

            #conexión          
            cur = mysql.connection.cursor()

            #Esto es para verificar si el correo ya existe. 
            cur.execute("SELECT * FROM encuestado WHERE email LIKE %s",[email])

            account = cur.fetchone()

            #Si el correo no existe entonces te deja registrarte.   
            if account is None: 
               cur.execute('INSERT INTO encuestado (prim_nom,seg_nom,ap_pat,ap_mat,email,password) VALUES (%s, %s, %s, %s, %s, %s)'
               ,(nombre,nombre2,apellido,apellido2,email,password))   
               mysql.connection.commit()

               flash("Registrado exitosamente")
               return redirect(url_for("register"))

            #Si el correo ya existe te manda error y te regresa a la de registro. 
            else:
                 flash("El correo ya existe")
                 return redirect(url_for("register"))
       else:
            flash("Por favor, ingrese sus datos")
            return redirect(url_for("register")) 
    else: 
        return render_template('register.html')