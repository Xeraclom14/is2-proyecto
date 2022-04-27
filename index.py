from __main__ import app

@app.route('/')
def Index():
    #cur = mysql.connection.cursor()
    #cur.execute("INSERT INTO `encuestador`(`ap_pat`, `ap_mat`, `prim_nom`,`seg_nom`,`email`) VALUES ('V','C','J','A','j@gmail.com')")
    #mysql.connection.commit()
    return "INDEX"
