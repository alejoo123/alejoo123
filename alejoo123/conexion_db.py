import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        host="localhost",           # Cambia si no estás usando localhost
        database="terminal_terrestre",   
        user="postgres",          
        password="RgLd28818"        
    )

def verificar_usuario_en_bd(usuario, clave):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT cedula, nombre, apellido, correo, clave, rol
            FROM usuarios
            WHERE (LOWER(nombre) = LOWER(%s) OR LOWER(correo) = LOWER(%s)) AND clave = %s
        """, (usuario, usuario, clave))

        resultado = cursor.fetchone()
        
        if resultado:
            return {
                "cedula": resultado[0],
                "nombre": resultado[1],
                "apellido": resultado[2],
                "correo": resultado[3],
                "clave": resultado[4],
                "rol": resultado[5]
            }
        return None
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return None
    finally:
        conn.close()