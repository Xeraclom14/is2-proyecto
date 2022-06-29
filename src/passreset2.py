from sqlite3 import connect
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

from __main__ import app, mysql, mail

@app.route('/passreset2/<id>', methods=['GET', 'POST'])
def passreset2(id):

    if 'loggedin' in session:
        return(render_template("403.html"))

    if request.method == 'POST': 
       #Se ingreso una password
       if(request.form['password'] != ""):
            
            nuevapass = request.form['password']
            
            #conexión          
            cur = mysql.connection.cursor()

            #Esto es para verificar si el correo existe. 
            cur.execute("UPDATE encuestado SET password = %s WHERE id_encuestado = %s;", (nuevapass, id))
            mysql.connection.commit()
                
            flash("success","Se ha cambiado la contraseña existosamente.")
            return redirect(url_for("login"))
       else:
            flash("warning","Por favor, ingrese su nueva contraseña.")
            return(render_template("passreset2.html", id = id))
    else: 
        return(render_template("passreset2.html", id = id))