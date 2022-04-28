from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import uuid

app = Flask(__name__)

###encuestador id
###INSERT INTO `encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`) VALUES ('V','C','J','A','1')
e_id = 1


###BD
app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''

###Nombre de la BD
app.config['MYSQL_DB'] = 'is2_proyecto'
mysql = MySQL(app)

###datos de sesión
app.secret_key = 'mysecretkey'


###crea un usuario en ala base de datos
import delete
import edit
import form
import forms
import index
import login
import stats

if __name__ == '__main__':
    app.run(port = 5000, debug = True)