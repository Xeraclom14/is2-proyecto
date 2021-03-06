from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app, mysql

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   #session.pop('loggedin', None)
   #session.pop('id', None)
   #session.pop('username', None)
   session.clear()
   # Redirect to login page
   return redirect(url_for('Index'))