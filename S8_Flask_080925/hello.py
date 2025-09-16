from flask import Flask, render_template
import pymysql.cursors
from flask import request
import os
app = Flask(__name__)

def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='dawb_bd',
            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except:
        return None    
           

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/prueba2")
def dibujartablero(): 
    strHTML = '<html><head><title>Reporte Ajedrez</title></head>'
    strHTML += '<body>'
    strHTML += "<table border='1' style='border-collapse: collapse; text-align: center;'>"

    # Definir filas iniciales
    fila0 = ["TN", "CN", "AN", "RN", "DN", "AN", "CN", "TN"]  # piezas negras
    fila1 = ["PN"] * 8  # peones negros
    fila6 = ["PB"] * 8  # peones blancos
    fila7 = ["TB", "CB", "AB", "RB", "DB", "AB", "CB", "TB"]  # piezas blancas

    for varY in range(8):  # Filas del tablero
        strHTML += '<tr>'
        for varX in range(8):  # Columnas
            if varY == 0:
                contenido = fila0[varX]
            elif varY == 1:
                contenido = fila1[varX]
            elif varY == 6:
                contenido = fila6[varX]
            elif varY == 7:
                contenido = fila7[varX]
            else:
                contenido = " "
            strHTML += '<td width="50" height="50">%s</td>\n' % contenido
        strHTML += '</tr>'

    strHTML += '</table>'
    strHTML += '</body>'
    strHTML += '</html>'

    return strHTML


@app.route("/probarconexion")
def probarConexion():
    try:
        connection = obtenerconexion()
        if connection is not None:
            return "<p>Conexión exitosa</p>"
        else:
            return "<p>Ocurrió un error</p>"
    except Exception as e:
        return "<p>%s</p>" % repr(e)
    
""" @app.route("/probarconexion")
def probarConexion():
    try:
        connection = obtenerConexion()
        if connection is not None:
            return "<p>Conexión exitosa</p>"
        else:
            return "<p>Ocurrió un error</p>"
    except Exception as e:
        return "<p>%s</p>" % repr(e)

@app.route("/probarinsertar")
def probarinsertar():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='dawa_bd',
            cursorclass=pymysql.cursors.DictCursor
        )
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    # Crear un nuevo registro
                    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
                connection.commit()
            return "<p>Registro insertado correctamente</p>"
        else:
            return "<p>Ocurrió un error</p>"
    except Exception as e:
        return "<p>%s</p>" % repr(e) """

@app.route("/probarleer")
def probarleer():
    try:
        connection = obtenerconexion()
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    # Leer un solo registro
                    sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
                    cursor.execute(sql, ('webmaster@python.org',))
                    result = cursor.fetchone()
                    
            return "<p>Datos del registro: id es <b>%s</b> y password es <b>%s</b></p>" % (result["id"], result["password"])

        else:
            return "<p>Ocurrió un error</p>"
    except Exception as e:
        return "<p>%s</p>" % repr(e)

@app.route("/probarinsertarparam/<string:email>/<string:password>")
def probarinsertarparam(email,password):
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='dawb_bd',
            cursorclass=pymysql.cursors.DictCursor
        )
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    # Crear un nuevo registro
                    sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
                    cursor.execute(sql, (email, password))
                connection.commit()
            return "<p>Registro correcto con parámetros</p>"
        else:
            return "<p>Ocurrió un error</p>"
    except Exception as e:
        return "<p>%s</p>" % repr(e)
    
    

    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='dawa_bd',
            cursorclass=pymysql.cursors.DictCursor
        )
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    # Traer id, email y password
                    sql = "SELECT `id`, `email`, `password` FROM `users` WHERE `id`=%s"
                    cursor.execute(sql, (id,))
                    result = cursor.fetchone()
                    
                    if result is None:
                        return "<p>No se encontró un usuario con ese ID</p>"
                    
                    return render_template("hello.html", person=result["email"])
        else:
            return "<p>Ocurrió un error con la conexión</p>"
    except Exception as e:
        return f"<p>Error: {repr(e)}</p>"

@app.route('/hello/<int:id>')     
def hello(id):   # 👈 aquí debe recibir 'id'
    try:
        connection = obtenerconexion()
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    # Traer id, email y password
                    sql = "SELECT `id`, `email`, `password` FROM `users` WHERE `id`=%s"
                    cursor.execute(sql, (id,))
                    result = cursor.fetchone()
                    
                    if result is None:
                        return "<p>No se encontró un usuario con ese ID</p>"
                    
                    return render_template("hello.html", person=result["email"])
        else:
            return "<p>Ocurrió un error con la conexión</p>"
    except Exception as e:
        return f"<p>Error: {repr(e)}</p>"


@app.route("/procesarregistrousuario", methods=['POST'])
def procesarregistrousuario():
    try:
        email = request.form['email']
        password = request.form['password']
        file = request.files['file']
        connection = obtenerconexion()

        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    # Crear un nuevo registro
                    sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
                    cursor.execute(sql, (email, password))
                connection.commit()
                
        if file and file.filename != '':
            file.save(os.path.join('./uploads', file.filename))
            archivo = open('./uploads/' + file.filename)
            c=0
            for linea in archivo:
                c+=1
        return render_template('hello.html', mensaje='Registrado Correctamente. %s líneas' % c, status=1)

    except Exception as e:
        return render_template('hello.html', mensaje=repr(e), status=0)     