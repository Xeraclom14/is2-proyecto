from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app
from __main__ import mysql

@app.route('/forms')
def forms():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM encuesta")
    datos = cur.fetchall()
    mysql.connection.commit()
    #print(datos)
    return render_template('forms.html', forms = datos)