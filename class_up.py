from datetime import datetime




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
    def __init__(self, cedula, nombre, apellido, correo_electronico, edad, codigo, ubicacion, clave):
        super().__init__(cedula, nombre, apellido, correo_electronico, edad, clave)
        self.codigo = codigo
        self._ubicacion = ubicacion
    @property
    def ubicacion(self):
        return self._ubicacion        


        
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
        self._registrar_evento(f"Adiministrador agrego al empleado {empleado.nombre} {empleado.apellido}")
    def eliminar_empleado(self, empleado: Empleado):
        self._registrar_evento(f"Administrador elimino al empleado {empleado.nombre} {empleado.apellido}")
    def ver_historico_ventas(self):
        self._registrar_evento("Administrador consulto historico de ventas")
        try:
            with open("historico_ventas.txt", "r") as archivo:
                return archivo.read()
        except FileNotFoundError:
            return "no hay registros de venta aun"

            
class Terminal:
    def __init__(self, ID_Ubicacion: int, ubicacion: str):
        self.ID_Ubicacion = ID_Ubicacion
        self.ubicacion = ubicacion
         # Agregación
        self._empleados = []
    
    def recibir_transporte(self, transporte):
        print(f"Recibiendo el transporte: {transporte.modelo} en terminal {self.ubicacion}")
    def entrada_empleado(self, empleado):
        self._empleados.append(empleado)
        print(f"Empleado {empleado.nombre} registrado en terminal {self.ubicacion}")   
        
class Transporte(Terminal):
    def __init__(self, ID_Ubicacion, ubicacion, disco:str, modelo:str, carroceria:str, chasis:str, ID_socio:int, nombre_socio:str, ID_operador:int):
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
        
class Frecuencia(Transporte):
    def __init__(self, ID_Ubicacion, ubicacion, disco, modelo, carroceria, chasis, ID_socio, nombre_socio, ID_operador,  terminal_salida:str, terminal_llegada:str, horario: str):
        super().__init__(ID_Ubicacion, ubicacion, disco, modelo, carroceria, chasis, ID_socio, nombre_socio, ID_operador)       
        self.terminal_salida = terminal_salida
        self.terminal_llegada = terminal_llegada
        self.horario = horario
        #metodos
    def cambio_de_horario(self, nuevo_horario: str):
        self._horario = nuevo_horario
        print(f"Horario actualizado a: {nuevo_horario}")    
        
class Operadores(Empleado):
    def __init__(self, cedula, nombre, apellido, correo_electronico, edad, ID_Empleado, ubicacion, tipo_empleado:str, puntos_licencia:int):
        super().__init__(cedula, nombre, apellido, correo_electronico, edad, ID_Empleado, ubicacion)      
        self.tipo_empleado = tipo_empleado
        self.puntos_licencia = puntos_licencia
        #metodos
    def cambio_unidad(self, nueva_unidad: str):
        print(f"Operador {self.nombre} ha cambiado a la unidad {nueva_unidad}") 
        #polimorfismo 
    def mostrar_info(self):
        print(f"Operador: {self.nombre} ({self.tipo_empleado}), Puntos licencia: {self.puntos_licencia}")  
        
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

#Inyeccion de dependencia 
class ServicioCifrado:
    def cifrar(self):
        print("Informacion cifrada correctamente.")

class PasarelaDePagos:
    def __init__(self, ID_pasarela: int, tasa_comision: float, fecha_configuracion: str, cifrador= None):
        self.ID_pasarela = ID_pasarela
        self.tasa_comision = tasa_comision
        self.fecha_configuracion = fecha_configuracion
        self._cifrador = cifrador or ServicioCifrado()


    def procesamiento_de_transaccion(self, gestor_pago: GestorDePagos):
        self._cifrado.cifrar()
        comision = gestor_pago.monto * self.tasa_comision
        total = gestor_pago.monto + comision
        print(f"💳 Procesando transacción para {gestor_pago.nombre}.\n"
              f"Monto: ${gestor_pago.monto}, Comisión: ${comision:.2f}, Total: ${total:.2f}")
       
