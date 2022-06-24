from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask import send_from_directory
from flask_mysqldb import MySQL
from flask_mail import Mail
import os
import mail_config
from flask_login import LoginManager

app = Flask(__name__)

###BD
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''

###Nombre de la BD
app.config['MYSQL_DB'] = 'is2_proyecto'
mysql = MySQL(app)

###datos de sesión
#La clave secreta.
app.secret_key = 'ffc5c7a327818c3193a6b640'

###Mail de la aplicacion
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_DEFAULT_SENDER'] = mail_config.MAIL_USER
app.config['MAIL_USERNAME'] = mail_config.MAIL_USER
app.config['MAIL_PASSWORD'] = mail_config.MAIL_PASSWORD
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#@app.before_request
#def make_session_permanent():
#    session.permanent = False

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

#Agregar cada archivo.py recientemente creado
import src.delete
import src.edit
import src.form
import src.forms
import src.results
import src.index
import src.login
import src.logout
import src.register
import src.loginadmin
import src.profile

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port = 5008, debug = True)

