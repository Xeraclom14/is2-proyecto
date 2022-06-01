from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql


@app.route('/')
def Index():
    if 'loggedin' in session:
        print(session)
        tiposesion = session['type']
        #print("Estamos viendo a un " + tiposesion)

        #hay alguien conectado.
        #que sucede si es un encuestador?
        if(tiposesion == "encuestador"):
            return render_template('encuestadores/index.html', username=session['username'])
        
        #acá se escribe el código para alguien registrado
        return render_template('encuestados/index.html', username=session['username'])
        

    #si no, no hay problema.
    return render_template('index.html')