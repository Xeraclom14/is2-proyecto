from attr import asdict
from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask import send_from_directory
from flask_mysqldb import MySQL
import uuid
import os
from flask_login import LoginManager

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
#La clave secreta, esto es importante.
app.secret_key = 'ffc5c7a327818c3193a6b640'

#funcionalidad de sesión
#login_manager = LoginManager()
#login_manager.init_app(app)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.get(user_id)

#@app.before_request
#def make_session_permanent():
#    session.permanent = False



@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


###crea un usuario en ala base de datos
import delete
import edit
import form
import forms
import index
import login
import stats
import logout
import register

if __name__ == '__main__':
    app.run(port = 5000, debug = True)
