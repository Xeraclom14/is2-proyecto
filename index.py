from flask import Flask, flash, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

from __main__ import app
from __main__ import mysql

@app.route('/')
def Index():
    #cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO `encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`,`password`) VALUES ('V','C','J','A','j@gmail.com','asd')")
    #mysql.connection.commit()
    return "INDEX"
