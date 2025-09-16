
import pymysql.cursors
from flask import request
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def obtenerconexion():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='practicando',
            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except:
        return None 
    
    
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
    
    
    
@app.route("/insertardisco/<codigo>/<nombre>/<artista>/<float:precio>/<genero>")
def insertarproducto(codigo, nombre, artista, precio, genero):
    try:
        connection = obtenerconexion()
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO discos (codigo, nombre, artista, precio, genero) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (codigo, nombre, artista, precio, genero))
                connection.commit()
            return f"<p>Producto '{nombre}' insertado correctamente</p>"
        else:
            return "<p>Ocurrió un error con la conexión</p>"
    except Exception as e:
        return f"<p>Error: {repr(e)}</p>"    
    
    
@app.route("/nuevo_disco")
def formulario_disco():
    
    return render_template("formulario_discos.html")    

@app.route("/guardar_disco", methods=["POST"] )
def guardar_disco():
    """
    Esta ruta recibe los datos del formulario y los inserta en la BD.
    """
    codigo = request.form['codigo']
    nombre = request.form['nombre']
    artista = request.form['artista']
    precio = request.form['precio']
    genero = request.form['genero']
    file = request.files['file']
    
    
    try:
        connection = obtenerconexion()
        if connection is not None:
            
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO discos (codigo, nombre, artista, precio, genero) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (codigo, nombre, artista, float(precio), genero))
                    connection.commit()
                    
        if file and file.filename != '':
            file.save(os.path.join('./uploads', file.filename))
            archivo = open('./uploads/' + file.filename)
            c=0
            for linea in archivo:
                c+=1            
            
           
            
            return f"<h1>¡Éxito!</h1><p>El disco '{nombre}' ha sido insertado correctamente.</p><a href='/nuevo_disco'>Insertar otro</a>"
        else:
            return "<h1>Error</h1><p>No se pudo conectar a la base de datos.</p>"
    except Exception as e:
        return f"<h1>Error</h1><p>Ocurrió un error al insertar: {repr(e)}</p>"