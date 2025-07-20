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
            SELECT * FROM usuarios
            WHERE (LOWER(nombre) = LOWER(%s) OR LOWER(correo) = LOWER(%s)) AND clave = %s
        """, (usuario, usuario, clave))

        resultado = cursor.fetchone()
        
        if resultado:
            # Asignación genérica - ajustar según tus columnas reales
            return {
                "id": resultado[0],        # Primera columna
                "nombre": resultado[1],    # Segunda columna
                "apellido": resultado[2],  # Tercera columna
                "correo": resultado[3],    # Cuarta columna
                "clave": resultado[4],    # Quinta columna
                "rol": resultado[5]       # Sexta columna
            }
        return None
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return None
    finally:
        conn.close()