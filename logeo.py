from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import uuid

from __main__ import app
from __main__ import mysql

@app.route('/login', methods=['GET', 'POST'])
def logeo():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'uname' in request.form and 'psw' in request.form:

        # Create variables for easy access
        username = request.form['uname']
        password = request.form['psw']        

        # Check if account exists using MySQL
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Encuestador WHERE email = %s AND password = %s', (username, password,))

        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            # Redirigir a pag principal
            return 'Logged in successfully!'

        else:
            #Cuenta incorrecta
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg='')