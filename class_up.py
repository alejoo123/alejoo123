from datetime import datetime
import csv
from abc import ABC, abstractmethod
import os
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql, extras
from ttkbootstrap.tableview import Tableview
import ttkbootstrap as tb
from conexion_db import obtener_conexion

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        try:
            self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="terminal_terrestre",  
            user="postgres",        
            password="RgLd28818"         
            )
            self.conn.autocommit = False
        except Exception as e:
            raise ConnectionError(f"Error al conectar a PostgreSQL: {e}")
    
    def get_cursor(self):
        return self.conn.cursor(cursor_factory=extras.DictCursor)
    
    def close(self):
        if self.conn:
            self.conn.close()
            self._instance = None
    
    def execute_query(self, query, params=None, fetch=False):
        cursor = self.get_cursor()
        try:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

# Singleton para la conexión
db = Database()


class Persona:
    def __init__(self, cedula:int, nombre:str, apellido:str, correo_electronico:str, edad:int, clave:str):
        self._cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.correo_electronico = correo_electronico
        self.edad  = edad
        self._clave = clave
    @property
    def clave(self):
        return self._clave
        #constructores
    @clave.setter
    def set_clave(self, clave):
        self._clave = clave
        
        
class Empleado(Persona):
    
    def __init__(self, cedula, nombre, apellido, correo_electronico=None, correo=None, edad=0, codigo=0, ubicacion="Terminal", clave=""):
            # Permite ambos nombres: 'correo_electronico' o 'correo'
            correo_final = correo_electronico if correo_electronico is not None else correo
            if correo_final is None:
                raise ValueError("Se requiere un correo electrónico")
                
            super().__init__(cedula, nombre, apellido, correo_final, edad, clave)
            self.codigo = codigo
            self._ubicacion = ubicacion
            self.registrar_evento(f"Empleado creado: {self.nombre}")
        
    @property
    def ubicacion(self):
        return self._ubicacion
        
    def registrar_evento(self, mensaje: str):
        """Método para registrar eventos de auditoría"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        linea = f"[{timestamp}] {mensaje}\n"
        with open("auditoria.txt", "a") as archivo:
            archivo.write(linea)
    
    @staticmethod
    def get_all():
        from conexion_db import obtener_conexion
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT cedula, nombre, apellido, correo, edad, codigo, ubicacion, clave FROM usuarios WHERE rol = 'empleado'")
        empleados = []
        for row in cursor.fetchall():
            empleado = Empleado(
                cedula=row[0],
                nombre=row[1],
                apellido=row[2],
                correo_electronico=row[3],
                edad=row[4],
                codigo=row[5],
                ubicacion=row[6],
                clave=row[7]
            )
            empleados.append(empleado)
        conn.close()
        return empleados
    
    @classmethod
    def save(cls, empleado_data):
        """Guarda un nuevo empleado en la base de datos"""
        from conexion_db import obtener_conexion
        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (cedula, nombre, apellido, correo, edad, codigo, ubicacion, clave, rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'empleado')
                """, (
                empleado_data['cedula'],
                empleado_data['nombre'],
                empleado_data['apellido'],
                empleado_data['correo_electronico'],
                empleado_data['edad'],
                empleado_data['codigo'],
                empleado_data['ubicacion'],
                empleado_data['clave']
            ))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
     
class Usuario(Persona):
    def __init__(self, cedula, nombre, apellido, correo_electronico, edad):
        super().__init__(cedula, nombre, apellido, correo_electronico, edad)

        
class Administrador(Empleado):
    def __init__(self, cedula, nombre, apellido, correo_electronico, edad, ID_Empleado, ubicacion, ID_Administrador:int, direccion:str, clave:str = "1234"):
        super().__init__(cedula, nombre, apellido, correo_electronico, edad, ID_Empleado, ubicacion, clave)
        self.ID_Administrador = ID_Administrador
        self.direccion = direccion
        self._clave = clave
        

        #metodos
    def cambio_credenciales(self):
        print("Cambiando credenciales del sistema...")
    def auditoria(self):
        print("Realizando auditoria del sistema...")
        #polimorfismo
    def mostrar_info(self):
        print(f"Administrador: {self.nombre} {self.apellido}, Dirección: {self.direccion}")
        
        
    def registrar_evento(self, mensaje: str):
        timestamp= datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        linea = f"[{timestamp}] {mensaje}\n"
        with open("auditoria.txt", "a") as archivo:
            archivo.write(linea)
    def revisar_solicitud_cambio_credenciales(self):
        self._registrar_evento("Administrador reviso solicitud de cambio de credenciales")
    def agregar_empleado(self, empleado: Empleado):
        self.registrar_evento(f"Adiministrador agrego al empleado {empleado.nombre} {empleado.apellido}")
    def eliminar_empleado(self, empleado: Empleado):
        self.registrar_evento(f"Administrador elimino al empleado {empleado.nombre} {empleado.apellido}")
    def ver_historico_ventas(self):
        self.registrar_evento("Administrador consulto historico de ventas")
        try:
            with open("historico_ventas.txt", "r") as archivo:
                return archivo.read()
        except FileNotFoundError:
            return "no hay registros de venta aun"

#Patron Command

class Comando(ABC):
    @abstractmethod
    def ejecutar(self):
        pass
    

class ComandoAgregarEmpleado(Comando):
    def __init__(self, admin, empleado_data):
        self.admin = admin
        # Normalizamos los nombres de campos
        self.empleado_data = {
            'cedula': empleado_data.get('cedula'),
            'nombre': empleado_data.get('nombre'),
            'apellido': empleado_data.get('apellido'),
            'correo_electronico': empleado_data.get('correo') or empleado_data.get('correo_electronico'),
            'edad': int(empleado_data.get('edad', 0)),
            'codigo': empleado_data.get('codigo', 0),
            'ubicacion': empleado_data.get('ubicacion', 'Terminal'),
            'clave': empleado_data.get('clave', '')
        }
    
    def ejecutar(self):
        try:
            
            # Lógica para guardar en la base de datos
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuarios (cedula, nombre, apellido, correo, edad, codigo, ubicacion, clave, rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'empleado')
            """, (
                self.empleado_data['cedula'],
                self.empleado_data['nombre'],
                self.empleado_data['apellido'],
                self.empleado_data['correo_electronico'],
                self.empleado_data['edad'],
                self.empleado_data['codigo'],
                self.empleado_data['ubicacion'],
                self.empleado_data['clave']
            ))
            conn.commit()
            conn.close()
            
            # Registramos el evento de auditoría
            self.admin.registrar_evento(
                f"Empleado agregado: {self.empleado_data['nombre']} {self.empleado_data['apellido']}"
            )
            return True, "Empleado agregado correctamente"
        except Exception as e:
            return False, f"Error al agregar empleado: {str(e)}"


class ComandoEliminarEmpleado(Comando):
    
    def __init__(self, admin, cedula):
        self.admin = admin
        self.cedula = cedula
    
    def ejecutar(self):
        try:
            Empleado.delete(self.cedula)
            self.admin.registrar_evento(f"Eliminó empleado con cédula: {self.cedula}")
            return True, "Empleado eliminado correctamente"
        except Exception as e:
            return False, str(e)

class ComandoVerHistoricoVentas(Comando):
    
    def __init__(self, admin):
        self.admin = admin
    
    def ejecutar(self):
        try:
            query = """
            SELECT v.id, v.fecha_hora, e.nombre, e.apellido, 
                   v.destino, v.hora_salida, v.disco_bus, 
                   v.precio, v.metodo_pago
            FROM ventas v
            JOIN empleados e ON v.id_empleado = e.id
            ORDER BY v.fecha_hora DESC
            """
            ventas = db.execute_query(query, fetch=True)
            
            # Crear ventana para mostrar resultados
            ventana = tb.Toplevel(title="Histórico de Ventas")
            ventana.geometry("1200x600")
            
            # Configurar columnas
            columns = [
                {"text": "ID", "stretch": False, "width": 50},
                {"text": "Fecha/Hora", "width": 150},
                {"text": "Empleado", "width": 150},
                {"text": "Destino", "width": 100},
                {"text": "Hora Salida", "width": 100},
                {"text": "Bus", "width": 100},
                {"text": "Precio", "width": 80},
                {"text": "Método Pago", "width": 100}
            ]
            
            # Preparar datos para la tabla
            rowdata = []
            for v in ventas:
                rowdata.append((
                    v['id'],
                    v['fecha_hora'].strftime('%Y-%m-%d %H:%M'),
                    f"{v['nombre']} {v['apellido']}",
                    v['destino'],
                    v['hora_salida'],
                    v['disco_bus'],
                    f"${v['precio']:.2f}",
                    v['metodo_pago']
                ))
            
            # Crear la tabla
            table = Tableview(
                master=ventana,
                coldata=columns,
                rowdata=rowdata,
                paginated=True,
                searchable=True,
                bootstyle="primary",
                height=20
            )
            table.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Agregar footer con resumen
            total_ventas = sum(v['precio'] for v in ventas)
            footer = tb.Frame(ventana)
            footer.pack(fill="x", pady=5)
            
            tb.Label(
                footer,
                text=f"Total de ventas: {len(ventas)} | Ingresos totales: ${total_ventas:.2f}",
                bootstyle="info"
            ).pack(side="left")
            
            self.admin.registrar_evento("Consultó histórico de ventas")
            return True, "Consulta exitosa"
            
        except Exception as e:
            print(f"Error al mostrar histórico: {e}")
            return False, str(e)
            
class Terminal:
    def __init__(self, ID_Ubicacion: int, ubicacion: str):
        self.ID_Ubicacion = ID_Ubicacion
        self.ubicacion = ubicacion
        self._empleados = []
    
    def recibir_transporte(self, transporte):
        print(f"Recibiendo el transporte: {transporte.modelo} en terminal {self.ubicacion}")
    
    def entrada_empleado(self, empleado):
        self._empleados.append(empleado)
        print(f"Empleado {empleado.nombre} registrado en terminal {self.ubicacion}") 
   
        
class Transporte(Terminal):
    def __init__(self, ID_Ubicacion, ubicacion, disco: str, modelo: str, carroceria: str, chasis: str, ID_socio: int, nombre_socio: str, ID_operador: int):
        super().__init__(ID_Ubicacion, ubicacion)
        self.disco = disco
        self.modelo = modelo
        self.carroceria = carroceria
        self.chasis = chasis
        self.ID_socio = ID_socio
        self.nombre_socio = nombre_socio
        self.ID_operador = ID_operador
    
    def asignar_ruta(self, ruta):
        print(f"Ruta {ruta} asignada al transporte {self.disco}")
    
    def operarla(self):
        print(f"Transporte {self.disco} está en operación.")
    
    def tiempo_llegada(self, minutos):
        print(f"Tiempo estimado de llegada: {minutos} minutos")
   
        
class Frecuencia:
    def __init__(self, origen, destino, hora_salida, bus_asignado):
        self.origen = origen
        self.destino = destino
        self._hora_salida = hora_salida
        self.bus_asignado = bus_asignado
        self.observadores = []

    def agregar_observador(self, observador):
        self.observadores.append(observador)

    def quitar_observador(self, observador):
        self.observadores.remove(observador)

    def notificar_observadores(self, mensaje):
        for observador in self.observadores:
            observador.actualizar(mensaje)

    @property
    def hora_salida(self):
        return self._hora_salida

    @hora_salida.setter
    def hora_salida(self, nueva_hora):
        if nueva_hora != self._hora_salida:
            mensaje = f"La hora de salida ha cambiado de {self._hora_salida} a {nueva_hora}"
            self._hora_salida = nueva_hora
            self.notificar_observadores(mensaje)
        
        
class OperadorBus(Persona):
    def __init__(self, cedula, nombre, apellido, correo_electronico, edad, puntos_licencia, esta_apto, id, clave=""):
        super().__init__(cedula, nombre, apellido, correo_electronico, edad, clave)
        self.puntos_licencia = puntos_licencia
        self.esta_apto = esta_apto
        self.id = id

    @property
    def sacar_datos(self):
        return self.nombre 
     
        
class Boleto(Usuario):
    def __init__(self, cedula, nombre, apellido, correo_electronico, edad,
                 horario:str, disco:str, destino:str):
        super().__init__(cedula, nombre, apellido, correo_electronico, edad)
        self.horario = horario
        self.disco = disco
        self.destino = destino
        
    def pedir(self):
        print(f"Boleto solicitado para {self.nombre} hacia {self.destino} en el bus {self.disco} a las {self.horario}.")   
        
        
class GestorDePagos(Boleto):
    def __init__(self, cedula: int, nombre: str, apellido: str, correo_electronico: str, edad: int,
                 horario: str, disco: str, destino: str,
                 ID_pago: int, fecha_hora_pago: str, monto: float):
        super().__init__(cedula, nombre, apellido, correo_electronico, edad, horario, disco, destino)
        self.ID_pago = ID_pago
        self.fecha_hora_pago = fecha_hora_pago
        self.monto = monto
    
    def generar_pago(self):
        print(f"Pago generado por {self.nombre}: ID {self.ID_pago}, Monto ${self.monto}, Fecha {self.fecha_hora_pago}")


def procesamiento_de_transaccion(self, gestor_pago:GestorDePagos):
    self.cifrado_de_pago()


class Reporte:
    def __init__(self, bus, operador, descripcion, fecha=None):
        self.bus = bus                # Objeto Bus
        self.operador = operador      # Objeto OperadorBus
        self.descripcion = descripcion
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def guardar_en_csv(self, ruta_archivo):
        # Guardar o agregar reporte al CSV
        with open(ruta_archivo, mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            # Si el archivo está vacío, escribir encabezados
            archivo.seek(0, 2)  # Ir al final del archivo
            if archivo.tell() == 0:
                escritor.writerow(["bus_numero_disco", "bus_placa", "operador_nombre", "descripcion", "fecha"])
            escritor.writerow([
                self.bus.numero_disco,
                self.bus.placa,
                self.operador.nombre,
                self.descripcion,
                self.fecha
            ])

    @staticmethod
    def cargar_reportes_desde_csv(ruta_archivo):
        reportes = []
        try:
            with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    reportes.append(fila)
        except FileNotFoundError:
            print("No existe el archivo de reportes.")
        return reportes


class EstadoDescuento(ABC):
    @abstractmethod
    def aplicar_descuento(self, monto: float) -> float:
        pass

class SinDescuento(EstadoDescuento):
    def aplicar_descuento(self, monto: float) -> float:
        return monto

class GrupoPrioritario(EstadoDescuento):
    def aplicar_descuento(self, monto: float) -> float:
        return monto * 0.5  # 50% de descuento

class Pago:
    def __init__(self, metodo, monto, cliente):
        self.metodo = metodo  # "efectivo", "tarjeta"
        self.monto = monto
        self.cliente = cliente

        # asignar estado descuento según cliente.grupo_prioritario
        if getattr(cliente, 'grupo_prioritario', False):
            self.estado_descuento = GrupoPrioritario()
        else:
            self.estado_descuento = SinDescuento()

    def calcular_monto_final(self):
        return self.estado_descuento.aplicar_descuento(self.monto)





#Inyeccion de dependencia 
class ServicioCifrado:
    def cifrar(self):
        print("Informacion cifrada correctamente.")


    def procesamiento_de_transaccion(self, gestor_pago: GestorDePagos):
        self._cifrado.cifrar()
        comision = gestor_pago.monto * self.tasa_comision
        total = gestor_pago.monto + comision
        print(f"💳 Procesando transacción para {gestor_pago.nombre}.\n"
              f"Monto: ${gestor_pago.monto}, Comisión: ${comision:.2f}, Total: ${total:.2f}")
       






