from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app
from __main__ import mysql

@app.route('/')
def Index():
    if 'loggedin' in session:
        print(session)
        tiposesion = session['type']
        #print("Estamos viendo a un " + tiposesion)

        #hay alguien conectado.
        #que sucede si es un encuestador?
        if(tiposesion == "encuestador"):
                return render_template('otroindex.html', username=session['username'])
        return render_template("logeado!")

    #si no, no hay problema.
    return render_template('index.html')