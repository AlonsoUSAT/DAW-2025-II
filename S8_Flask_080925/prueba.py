from flask import Flask, render_template
import pymysql.cursors

app = Flask(__name__)

@app.route("/probarconexion")
def probarConexion():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='prueba',
            cursorclass=pymysql.cursors.DictCursor
        )
        if connection is not None:
            return "<p>Conexión exitosa</p>"
        else:
            return "<p>Ocurrió un error</p>"
    except Exception as e:
        return "<p>%s</p>" % repr(e)
    
    
    
    
@app.route("/probarleer")
def probarleer():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='prueba',
            cursorclass=pymysql.cursors.DictCursor
        )
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    # Leer todos los productos
                    sql = "SELECT id, nombre, precio, stock, marca FROM producto"
                    cursor.execute(sql)
                    results = cursor.fetchall()   #  trae todas las filas
                    
            if results:
                html = "<h2>Lista de Productos</h2><ul>"
                for row in results:
                    html += (
                        f"<li>ID: {row['id']} - "
                        f"Nombre: {row['nombre']} - "
                        f"Precio: {row['precio']} - "
                        f"Stock: {row['stock']} - "
                        f"Marca: {row['marca']}</li>"
                    )
                html += "</ul>"
                return html
            else:
                return "<p>No hay productos registrados</p>"

        else:
            return "<p>Ocurrió un error</p>"
    except Exception as e:
        return f"<p>{repr(e)}</p>"

    
    
    
    
    
    
@app.route("/insertarproducto/<int:id>/<nombre>/<float:precio>/<int:stock>/<marca>")
def insertarproducto(id, nombre, precio, stock, marca):
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='prueba',
            cursorclass=pymysql.cursors.DictCursor
        )
        if connection is not None:
            with connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO producto (id, nombre, precio, stock, marca) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (id, nombre, precio, stock, marca))
                connection.commit()
            return f"<p>Producto '{nombre}' insertado correctamente</p>"
        else:
            return "<p>Ocurrió un error con la conexión</p>"
    except Exception as e:
        return f"<p>Error: {repr(e)}</p>"

@app.route("/buscarproducto/<cadena>")
def buscarproducto(cadena):
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3307,
            user='root',
            password='',
            database='prueba',
            cursorclass=pymysql.cursors.DictCursor
        )

        if connection is not None:
            with connection:
                with connection.cursor() as cursor:

                    # Función auxiliar para validar número
                    def es_numero(valor: str) -> bool:
                        try:
                            float(valor)
                            return True
                        except ValueError:
                            return False

                    if es_numero(cadena):
                        # Buscar coincidencias exactas en id, precio, stock
                        sql = """
                            SELECT * 
                            FROM producto 
                            WHERE id = %s
                               OR precio = %s
                               OR stock = %s
                               OR nombre LIKE %s
                               OR marca LIKE %s
                        """
                        # Convertir a número según el tipo
                        try:
                            entero = int(cadena)
                        except ValueError:
                            entero = None

                        numero = float(cadena)

                        cursor.execute(sql, (
                            entero,         # id exacto (solo si es entero)
                            numero,         # precio exacto
                            entero,         # stock exacto (solo si es entero)
                            f"%{cadena}%",  # nombre con LIKE
                            f"%{cadena}%"   # marca con LIKE
                        ))
                    else:
                        # Si no es número, buscar solo en texto
                        sql = """
                            SELECT * 
                            FROM producto 
                            WHERE nombre LIKE %s
                               OR marca LIKE %s
                        """
                        cursor.execute(sql, (
                            f"%{cadena}%",
                            f"%{cadena}%"
                        ))

                    result = cursor.fetchall()

                    if not result:
                        return f"<p>No se encontró ningún producto con '{cadena}'</p>"

                    # Construcción de tabla HTML
                    tabla = """
                        <table border='1' cellpadding='5'>
                        <tr><th>ID</th><th>Nombre</th><th>Precio</th><th>Stock</th><th>Marca</th></tr>
                    """
                    for row in result:
                        tabla += f"<tr><td>{row['id']}</td><td>{row['nombre']}</td><td>{row['precio']}</td><td>{row['stock']}</td><td>{row['marca']}</td></tr>"
                    tabla += "</table>"

                    return f"<h3>Resultados de la búsqueda '{cadena}'</h3>{tabla}"
        else:
            return "<p>Ocurrió un error con la conexión</p>"

    except Exception as e:
        return f"<p>Error: {repr(e)}</p>"
    