import ttkbootstrap as tb
from ttkbootstrap.constants import *
import re
import os
import smtplib
import random
from email.mime.text import MIMEText
from collections import Counter
from  class_up import *
import tkinter as tk
from tkinter import messagebox






#Empleado en sesion
#Variable para almacenar el empleado en sesion
# None se asigna al iniciar sesion, Luego se asigna al iniciar sesion
#Se usa para veriicar si un empleado esta en sesion o no
empleado_en_sesion = None
#empleados registrados
empleados_registrados = [
    Empleado(1, "Robert", "Garcia", "rg4867965@gmail.com", 20, 2004, "San Jacinto", "1234"),
    Empleado(2, "Andy", "Garcia", "andy@mail.com", 19, 2005, "Manta", "1234"),
]
#Administrador registrado
ADMIN = Administrador(1, "Jhonny", "Perez", "rg4867965@gmail.com", 19, 1001, "Guayaquil", 5001, "Av. Principal", "1234")
#Transportes disponibles
transportes_disponibles = [
    {
        "nombre": "Bus 13",
        "compañia": "Coop. Manabí",
        "ubicacion": "Bahía",
        "disco": "D-045",
        "modelo": "2015",
        "carroceria": "IMCE",
        "chasis": "Mercedes-Benz",
        "ubicacion_terminal": "Andén 1"
    },
    {
        "nombre": "Bus 3",
        "compañia": "Coop. Bahía",
        "ubicacion": "Portoviejo",
        "disco": "D-022",
        "modelo": "2018",
        "carroceria": "MARCOPOLLO",
        "chasis": "Volvo",
        "ubicacion_terminal": "Andén 2"
    },
    {
        "nombre": "Bus 8",
        "compañia": "Coop. Pacífico",
        "ubicacion": "Chone",
        "disco": "D-067",
        "modelo": "2020",
        "carroceria": "AYCO",
        "chasis": "Scania",
        "ubicacion_terminal": "Andén 3"
    },
    {
        "nombre": "Bus 10",
        "compañia": "Coop. Manabí",
        "ubicacion": "Pedernales",
        "disco": "D-031",
        "modelo": "2017",
        "carroceria": "IMCE",
        "chasis": "Mercedes-Benz",
        "ubicacion_terminal": "Andén 4"
    }
]











    
def verificar_credenciales(usuario, clave, ventana_login):
    if (usuario.lower() == ADMIN.nombre.lower() or usuario.lower() == ADMIN.correo_electronico.lower()) and clave == ADMIN.clave:
        messagebox.showinfo("Acceso concedido", "✅ Ingresaste como administrador. ---->")
        interfaz_admin(ventana_login)  # Llama la siguiente ventana luego de verificar credenciales
    else:
        messagebox.showinfo("Acceso denegado", "❌ Credenciales incorrectas.")

        
def verificar_credenciales_empe(usuario, clave, ventana_sesion_empleado):
    for emp in empleados_registrados:
        if (emp.nombre.lower() == usuario.lower() or emp.correo_electronico.lower() == usuario.lower()) and emp.clave == clave:
            global empleado_en_sesion
            empleado_en_sesion = emp
            messagebox.showinfo("Acceso concedido", "✅ Ingresaste como empleado. ---->")
            interfaz_empleado(ventana_sesion_empleado)
            return
    messagebox.showinfo("Acceso denegado", "❌ Credenciales Incorrectas.")






def interfaz_admin(ventana_login):
    print("Entrando a interfaz_admin") # depuracion
    ventana_login.withdraw()  # Oculta la ventana de login del administrador
    # Crea una nueva ventana para el panel de administrador
    ventana_admin = tb.Toplevel()
    ventana_admin.title("Panel de Administrador")
    ventana_admin.geometry("700x600")
    frame_fondo = tb.Frame(ventana_admin, bootstyle="light")
    frame_fondo.pack(fill="both", expand=True)
    
    def al_cerrar():
        ventana_login.deiconify()
        ventana_admin.destroy()
    ventana_admin.protocol("WM_DELETE_WINDOW", al_cerrar)
    
    # Etiqueta de título
    tb.Label(
        frame_fondo,
        text="Panel de Control del Administrador 👨‍💼",
        font=("Helvetica", 14, "bold"),
        bootstyle = "success",  # Estilo del texto
    ).pack(pady=15)

    # se ve el nombre del administrador de titulo
    tb.Label(
        frame_fondo, 
        text=f"👤 Administrador: {ADMIN.nombre} {ADMIN.apellido}",
        font=("Arial", 12, "bold"), 
        bootstyle = "info",  # Estilo del texto
        ).pack(pady=10)

    tb.Label(
        frame_fondo, 
        text="📋 Lista de empleados registrados:", 
        font=("Arial", 11), 
        bootstyle = "primary"  # Estilo del texto
        ).pack()

    lista = tk.Listbox(frame_fondo, width=50)
    lista.pack(pady=10)

    for emp in empleados_registrados:
        lista.insert(tk.END, f"{emp.nombre} {emp.apellido} - {emp.ubicacion}")
        

    # Boton para cambiar credenciales
    tb.Button(
        frame_fondo,
        text="Cambiar Credenciales",
        width=25,
        bootstyle = "outline-primary",  # Estilo del botón
        command = cambiar_credenciales_admin
    ).pack(pady=5)
    
    tb.Button(
        frame_fondo,
        text="Auditoria",
        width=25,
        bootstyle = "outline-primary",
        command = abrir_ventana_auditoria
    ).pack(pady=5)


    # Botón para cerrar sesión
    tb.Button(
        frame_fondo,
        text="Cerrar Sesión",
        width=25,
        bootstyle="outline-danger",  # Botón rojo para cerrar sesión
        command=ventana_admin.destroy # Cierra la ventana del administrador y vuelve al login
    ).pack(pady=20)

        
def abrir_login_admin():
    ventana_login = tb.Toplevel()
    ventana_login.title("Login Administrador")
    ventana_login.geometry("400x350")
    ventana.withdraw()  # Oculta la ventana principal al abrir el login del administrador
    

    
    tb.Label(ventana_login, text="Usuario:").pack(pady=5)
    entrada_usuario = tb.Entry(ventana_login)
    entrada_usuario.pack()

    tb.Label(ventana_login, text="Contraseña:").pack(pady=10)
    entrada_clave = tb.Entry(ventana_login, show="*")  # Oculta la clave
    entrada_clave.pack()
    
    # Etiqueta para recuperar contraseña
    tb.Label(ventana_login, 
             text="¿Olvidaste tu contraseña?"
             ).pack(pady=5) 
 
    # Botón para recuperar contraseña
    tb.Button(ventana_login,
            text="Recuperar contraseña", 
            bootstyle = "success", 
            command=lambda: recuperar_contraseña_administrador(
                    entrada_usuario.get(), ventana_login, [ADMIN]
            )).pack(pady=5)

    # Función para intentar el login                                    
    def intentar_login():
        usuario = entrada_usuario.get()
        clave = entrada_clave.get()
        verificar_credenciales(usuario, clave, ventana_login)  # Verifica las credenciales y abre la interfaz del administrador si son correctas
    # Botón para intentar el login
    tb.Button(ventana_login, text="Ingresar", command=intentar_login).pack(pady=10)
    
 
def recuperar_contraseña_administrador(usuario, abrir_login_admin, ADMIN):
    abrir_login_admin.withdraw()  # Oculta la ventana de login del empleado
    # Busca el correo del usuario en la lista de empleados
    correo = None
    print(f"Administrador ingresado: '{usuario}'")
    for emp in ADMIN:
        print(f"Comparando con: '{emp.nombre}' y '{emp.correo_electronico}'")
        if emp.nombre.lower().strip() == usuario.lower().strip() or emp.correo_electronico.lower().strip() == usuario.lower().strip():
            correo = emp.correo_electronico
            # Si se encuentra el correo, se sale del bucle
            break

    if not correo:
        nombres = ", ".join(emp.nombre for emp in ADMIN)
        messagebox.showerror("Error", f"Administrador no encontrado o sin correo registrado.\nNombres válidos: {nombres}")
        return
    
    # Si se encuentra el correo, abre la ventana de recuperación de contraseña
    ventana_recuperar_admin = tb.Toplevel()
    ventana_recuperar_admin.title("Recuperar contraseña")
    ventana_recuperar_admin.geometry("500x500")
    tb.Label(
        ventana_recuperar_admin, 
        text="Recuperar contraseña",
        bootstyle="info",  # Estilo del texto
        font = ("Times New Roman", 14, "bold"
        )).pack(pady=10)
    # Etiqueta y campo de entrada para el correo electrónico
    tb.Label(
        ventana_recuperar_admin, 
        text=f"Se enviará un PIN al correo: {correo}"
        ).pack(pady=5)
    
    # Variable para guardar el PIN generado
    pin_generado = [None]
    
    # Botón para enviar el PIN al correo electrónico
    def enviar_correo():
        pin = random.randint(100000, 999999)
        if enviar_pin_gmail(correo, pin):
            pin_generado[0] = pin  # Guarda el PIN generado
            # Muestra un mensaje de éxito
            messagebox.showinfo("Correo enviado", f"Se envió un PIN a {correo}.")
            # Aquí puedes pedir al usuario que ingrese el PIN recibido y verificarlo
            pedir_pin(pin_generado, ventana_recuperar_admin, correo)  
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo.")

    tb.Button(ventana_recuperar_admin, text="Enviar PIN", command=enviar_correo).pack(pady=10)
   
    
def pedir_pin(pin_generado, ventana_recuperar_admin, correo):
    ventana_pin_admin = tb.Toplevel()
    ventana_pin_admin.title("Verificar PIN")
    ventana_pin_admin.geometry("450x350")
    tb.Label(ventana_pin_admin, text="Ingrese el PIN recibido:").pack(pady=10)
    entrada_pin = tb.Entry(ventana_pin_admin)
    entrada_pin.pack(pady=5)
    
    def abrir_cambio_contraseña_admin():
        ventana_cambio_admin = tb.Toplevel()
        ventana_cambio_admin.title("Cambiar contraseña")
        ventana_cambio_admin.geometry("450x300")
        tb.Label(ventana_cambio_admin, text="Nueva contraseña:").pack(pady=10)
        entrada_nueva = tb.Entry(ventana_cambio_admin, show="*")
        entrada_nueva.pack(pady=5)
        tb.Label(ventana_cambio_admin, text="Confirmar contraseña:").pack(pady=10)
        entrada_confirmar = tb.Entry(ventana_cambio_admin, show="*")
        entrada_confirmar.pack(pady=5)

        def guardar_nueva():
            nueva = entrada_nueva.get()
            confirmar = entrada_confirmar.get()
            if not nueva or not confirmar:
                messagebox.showwarning("Campos vacíos", "Completa ambos campos.")
                return
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
            # Cambia la clave del administrador
            ADMIN.clave = nueva
            messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
            ventana_cambio_admin.destroy()
            abrir_login_admin()

        tb.Button(ventana_cambio_admin, text="Guardar", command=guardar_nueva).pack(pady=10)


def abrir_login_empleado():
    ventana_sesion_empleado = tb.Toplevel()
    ventana_sesion_empleado.title("Login Empleado")
    ventana_sesion_empleado.geometry("400x300")
    ventana.withdraw()  # Oculta la ventana principal al abrir el login del empleado
    
    tb.Label(ventana_sesion_empleado, text="Usuario:").pack(pady=5)
    entrada_empleado = tb.Entry(ventana_sesion_empleado)
    entrada_empleado.pack()
    
    tb.Label(ventana_sesion_empleado, text="Contraseña:").pack(pady=10)
    entrada_clave_empe = tb.Entry(ventana_sesion_empleado, show="*")  # Oculta la clave
    entrada_clave_empe.pack()
    
    tb.Label(ventana_sesion_empleado, text="¿Olvidaste tu contraseña?").pack(pady=5) 
    # Botón para recuperar contraseña
    tb.Button(
        ventana_sesion_empleado, 
        text="Recuperar contraseña", 
        bootstyle="success",
        command=lambda: recuperar_contraseña_empleado(entrada_empleado.get(), ventana_sesion_empleado)
        ).pack(pady=5)
    
    
    def intentar_login_empe():
        usuario = entrada_empleado.get()
        clave = entrada_clave_empe.get()
        verificar_credenciales_empe(usuario, clave, ventana_sesion_empleado)  # Verifica las credenciales y abre la interfaz del empleado si son correctas
    # Botón para intentar el login
    tb.Button(ventana_sesion_empleado, text="Ingresar", command=intentar_login_empe).pack(pady=10)
   
    
def recuperar_contraseña_empleado(usuario, abrir_login_empleado):
    abrir_login_empleado.withdraw()  # Oculta la ventana de login del empleado
    # Busca el correo del usuario en la lista de empleados
    correo = None
    print(f"Usuario ingresado: '{usuario}'")
    for emp in empleados_registrados:
        print(f"Comparando con: '{emp.nombre}' y '{emp.correo_electronico}'")  
        if emp.nombre.lower().strip() == usuario.lower().strip() or emp.correo_electronico.lower().strip() == usuario.lower().strip():
            correo = emp.correo_electronico
            # Si se encuentra el correo, se sale del bucle
            break

    if not correo:
        nombres = ", ".join(emp.nombre for emp in empleados_registrados)
        messagebox.showerror("Error", f"Usuario no encontrado o sin correo registrado.\nNombres válidos: {nombres}")
        return
    # Si se encuentra el correo, abre la ventana de recuperación de contraseña
    ventana_recuperar = tb.Toplevel()
    ventana_recuperar.title("Recuperar contraseña")
    ventana_recuperar.geometry("500x400")
    tb.Label(
        ventana_recuperar, 
        text="Recuperar contraseña",
        bootstyle="info",  # Estilo del texto
        font = ("Times New Roman", 14, "bold"
        )).pack(pady=10)
    # Etiqueta y campo de entrada para el correo electrónico
    tb.Label(
        ventana_recuperar, 
        text=f"Se enviará un PIN al correo: {correo}"
        ).pack(pady=5)
    
    # Variable para guardar el PIN generado
    pin_generado = [None]
    
    # Botón para enviar el PIN al correo electrónico
    def enviar_correo():
        pin = random.randint(100000, 999999)
        if enviar_pin_gmail(correo, pin):
            pin_generado[0] = pin  # Guarda el PIN generado
            # Muestra un mensaje de éxito
            messagebox.showinfo("Correo enviado", f"Se envió un PIN a {correo}.")
            # Aquí puedes pedir al usuario que ingrese el PIN recibido y verificarlo
            pedir_pin(pin_generado, ventana_recuperar, correo)  
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo.")

    tb.Button(ventana_recuperar, text="Enviar PIN", command=enviar_correo).pack(pady=10)
   
    
def pedir_pin(pin_generado, ventana_recuperar, correo):
    ventana_pin = tb.Toplevel()
    ventana_pin.title("Verificar PIN")
    ventana_pin.geometry("350x250")
    tb.Label(ventana_pin, text="Ingrese el PIN recibido:").pack(pady=10)
    entrada_pin = tb.Entry(ventana_pin)
    entrada_pin.pack(pady=5)

    def abrir_cambio_contraseña():
        ventana_cambio = tb.Toplevel()
        ventana_cambio.title("Cambiar contraseña")
        ventana_cambio.geometry("450x300")
        tb.Label(ventana_cambio, text="Nueva contraseña:").pack(pady=10)
        entrada_nueva = tb.Entry(ventana_cambio, show="*")
        entrada_nueva.pack(pady=5)
        tb.Label(ventana_cambio, text="Confirmar contraseña:").pack(pady=10)
        entrada_confirmar = tb.Entry(ventana_cambio, show="*")
        entrada_confirmar.pack(pady=5)

        def guardar_nueva():
            nueva = entrada_nueva.get()
            confirmar = entrada_confirmar.get()
            if not nueva or not confirmar:
                messagebox.showwarning("Campos vacíos", "Completa ambos campos.")
                return
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return

            # Buscar el empleado por correo y cambiar su clave
            for emp in empleados_registrados:
                if emp.correo_electronico == correo:
                    emp.clave = nueva # Cambia la clave del empleado
                    # Muestra un mensaje de éxito
                    messagebox.showinfo("Éxito", "Contraseña cambiada correctamente.")
                    ventana_cambio.destroy()
                    abrir_login_empleado()
                    return
            messagebox.showerror("Error", "No se encontró el empleado.")
            
        tb.Button(ventana_cambio, text="Guardar", command=guardar_nueva).pack(pady=10)
        
    # Botón para verificar el PIN ingresado
    def verificar_pin():
        if entrada_pin.get() == str(pin_generado[0]):
            messagebox.showinfo("Éxito", "PIN verificado. Ahora puedes cambiar tu contraseña.")
            ventana_pin.destroy()
            ventana_recuperar.destroy()
            # Aquí puedes abrir una ventana para cambiar la contraseña
            abrir_cambio_contraseña()
        else:
            messagebox.showerror("Error", "PIN incorrecto.")

    tb.Button(ventana_pin, text="Verificar", command=verificar_pin).pack(pady=10)

        
def enviar_pin_gmail(destinatario, pin):
    remitente = "rg4867965@gmail.com"  #tu correo
    clave = "atdz huoz spah hzzg"  # Usa la contraseña de aplicación real
    mensaje = MIMEText(f"Tu PIN de vterificación es: {pin}")
    mensaje['Subject'] = "Verificación de contraseña"
    mensaje['From'] = remitente
    mensaje['To'] = destinatario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(remitente, clave)
            servidor.sendmail(remitente, destinatario, mensaje.as_string())
        return True
    except Exception as e:
        print("Error enviando correo:", e)
        return False    
   
    
def cambiar_credenciales_admin():
    ventana_cambio = tb.Toplevel()
    ventana_cambio.title("Cambiar credenciales del Administrador")
    ventana_cambio.geometry("400x300")

    tb.Label(ventana_cambio, text="Nuevo Usuario:").pack(pady=5)
    entrada_nuevo_usuario = tb.Entry(ventana_cambio)
    entrada_nuevo_usuario.pack()

    tb.Label(ventana_cambio, text="Nueva clave:").pack(pady=5)
    entrada_nueva_clave = tb.Entry(ventana_cambio, show="*")
    entrada_nueva_clave.pack()

    def guardar_nuevas_credenciales():
        global ADMIN_USUARIO, ADMIN_CLAVE
        nuevo_usuario = entrada_nuevo_usuario.get()
        nueva_clave = entrada_nueva_clave.get()

        if nuevo_usuario and nueva_clave:
            ADMIN_USUARIO = nuevo_usuario
            ADMIN_CLAVE = nueva_clave
            messagebox.showinfo("Exito","✅ credenciales actualizadas correctamente.")
        else:
            messagebox.showwarning("Campos vacios", "Por favor complete todos los campos.")

    tb.Button(ventana_cambio, text="Guardar", command=guardar_nuevas_credenciales).pack(pady=10)

    
def abrir_ventana_auditoria():
    ventana_auditoria = tb.Toplevel()
    ventana_auditoria.title("Auditoria")
    ventana_auditoria.geometry("400x400")
    frame_fondo = tb.Frame(ventana_auditoria, bootstyle="light")
    frame_fondo.pack(fill="both", expand=True)
    

    tb.Label(
        frame_fondo, 
        text="Panel de Auditoria", 
        bootstyle="success",
        ).pack(pady=30)
    
    #boton1 Revisar solicitud de cambio de credenciales
    tb.Button(
        frame_fondo, 
        text="Resvisar solicitud de credenciales", 
        bootstyle="outline-primary", 
        command=lambda: (
        ADMIN.revisar_solicitud_cambio_credenciales(),
        messagebox.showinfo("Auditoria", "Solicitud de cambio de credenciales revisada.")
        )).pack(pady=10)
    
    
    #boton2 Agregar Empleado (solo registro de accion)
    tb.Button(
        frame_fondo, 
        text="Agregar empleado", 
        bootstyle="outline-primary", 
        command= lambda: (
        ADMIN.registrar_evento("Administrador agrego un nuevo"),
        messagebox.showinfo("Auditoria", "Nuevo empleado agregado.")
        )).pack(pady=10)
    
    #boton3 Eliminar Empleado (solo registro de accion)
    tb.Button(
        frame_fondo, 
        text="Eliminar empleado", 
        bootstyle="outline-primary", 
        command= lambda: (
        ADMIN.registrar_evento("Administrador elimino un empleado"),
        messagebox.showinfo("Auditoria", "Empleado eliminado.")
        )).pack(pady=10)
    
    #boton4 Ver historico de ventas
    tb.Button(
        frame_fondo, 
        text= "Ver historico de ventas", 
        bootstyle="outline-primary", 
        command = ver_historico_ventas
        ).pack(pady=10)


def ver_historico_ventas():
    # Verificar si el archivo de ventas existe y leerlo
    ruta = os.path.join(os.path.dirname(_file_), "historico_ventas.txt")
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el archivo de ventas.")
        return
    total_ventas = 0
    total_ganancias = 0.0
    clientes = []

    for linea in lineas:
        match_cliente = re.search(r"Pasajero: ([^|]+)", linea)
        match_precio = re.search(r"Precio: \$([0-9.]+)", linea)
        if match_cliente and match_precio:
            cliente = match_cliente.group(1).strip()
            precio = float(match_precio.group(1))
            clientes.append(cliente)
            total_ventas += 1
            total_ganancias += precio

    if not clientes:
        messagebox.showinfo("Sin datos", "No hay ventas registradas.")
        return

    # Cliente que más compró
    cliente_mas_compro = Counter(clientes).most_common(1)[0][0]

    resumen = (
        f"Cantidad total de ventas: {total_ventas}\n"
        f"Cliente que más compró: {cliente_mas_compro}\n"
        f"Total de ganancias: ${total_ganancias:.2f}"
    )
    messagebox.showinfo("Resumen de Ventas", resumen)


def interfaz_empleado(ventana_sesion_empleado):
    ventana_sesion_empleado.withdraw()  # Oculta la ventana de login del empleado
    # Crea una nueva ventana para el panel de empleado
    ventana_empleado= tb.Toplevel()
    ventana_empleado.title("Panel de empleado")
    ventana_empleado.geometry("1500x650")
    frame_fondo = tb.Frame(ventana_empleado, bootstyle="light")
    frame_fondo.pack(fill="both", expand=True) 
    
    tb.Label(
        frame_fondo,
        text=f"👨‍💼 Bienvenido {empleado_en_sesion.nombre} {empleado_en_sesion.apellido}",
        font=("Helvetica", 14, "bold"),
        bootstyle="success",  # Estilo del texto
    ).pack(pady=15)


    tb.Label(
        frame_fondo,
        text="Seleccione hora de salida",
        font=("Helvetica", 12, "bold"),
        bootstyle="primary",  # Estilo del texto
    ).pack(pady=10)

    contendor_horas = tb.Frame(frame_fondo, bootstyle="light")
    # Contenedor para los botones de horas
    contendor_horas.pack(pady=10)
    horas_disponibles=["5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
    # Función para seleccionar la hora y generar el boleto
    direcciones = [
        "Bahia", "Portoviejo", "chone", "Pedernales", "Bahia", "Portoviejo", "chone", "Pedernales",
        "Bahia", "Portoviejo", "chone", "Pedernales", "Bahia", "Portoviejo", "chone", "Pedernales", "Bahia"
    ]

    def seleccionar_hora(hora, direccion, ventana_empleado):
        ventana_empleado.withdraw()  # Oculta la ventana de emplea
        ventana_boleto = tb.Toplevel()
        ventana_boleto.title("Generar boleto")
        ventana_boleto.geometry("1000x500")
        frame_fondo_boleto = tb.Frame(ventana_boleto, bootstyle="light")
        frame_fondo_boleto.pack(fill="both", expand=True)

        bus_seleccionado= random.choice(transportes_disponibles)

        tb.Label (
            frame_fondo_boleto,
            text=f"Hora seleccionada: {hora}\nDireccion:{direccion}",
            font=("helvetica", 14, "bold"),
            bootstyle="info"  # Estilo del texto
        ).pack(pady=10)

        tb.Label(
            frame_fondo_boleto,
            text=f"Transporte asignado:",
            font=("helvetica", 12, "bold"),
            bootstyle="success"
        ).pack()

        atributos = (
            f"• Nombre: {bus_seleccionado['nombre']}",
            f"• Compañia: {bus_seleccionado['compañia']}",
            f"• Ubicación: {bus_seleccionado['ubicacion']}",
            f"• Disco: {bus_seleccionado['disco']}",
            f"• Modelo: {bus_seleccionado['modelo']}",
            f"• Carrocería: {bus_seleccionado['carroceria']}",
            f"• Chasis: {bus_seleccionado['chasis']}",
            f"• Ubicación en terminal: {bus_seleccionado['ubicacion_terminal']}"
        )

        for texto in atributos:
            tb.Label(
                frame_fondo_boleto,
                text=texto,
                font = ("Helvetica", 11),
                bootstyle="secondary"
            ).pack(pady=2)

        def generar_boleto():
            messagebox.showinfo("Boleto", "Boleto Generado")


        tb.Button(
            frame_fondo_boleto,
            text="Generar Boleto",
            bootstyle="outline-primary",  # Estilo del botón
            # Comando para generar el boleto
            width=18,
            padding=10,
            command=generar_boleto
        ).pack(pady=20)
        
        # Cuando se cierre la ventana de boleto, mostrar la ventana de empleado otra vez
        def al_cerrar():
            ventana_empleado.deiconify()
            ventana_boleto.destroy()
        ventana_boleto.protocol("WM_DELETE_WINDOW", al_cerrar)
        
    columnas = 4    
    #botones de hora
    for i, (hora, direccion) in enumerate(zip(horas_disponibles, direcciones)):
        fila = (i // columnas) * 2  # Cada hora ocupa dos filas (botón y dirección)
        columna = i % columnas

        # Botón de hora
        tb.Button(
            contendor_horas,
            text=hora,
            width=20,
            bootstyle="outline-primary",
            command=lambda h=hora, d=direccion: seleccionar_hora(h, d, ventana_empleado)
        ).grid(row=fila, column=columna, padx=10, pady=(10, 0))

        # Label de dirección debajo del botón
        tb.Label(
            contendor_horas,
            text=f"Dirección: {direccion}",
            font=("Arial", 9),
            bootstyle="info"
        ).grid(row=fila + 1, column=columna, padx=10, pady=(0, 10))






    
    
    
    
    
    
    
    
    
    
    
    




# Interfaz principal - Verde Tranquilo
ventana = tb.Window(themename="flatly")  # Puedes cambiar el tema si quieres
ventana.title("Sistema de Boletería - TERMINAL")
ventana.geometry("400x250")
ventana.configure(bg="#f4fbf4")  # Fondo verde muy claro


# Etiqueta
tb.Label(
    ventana,
    text="Hola de nuevo 👋, elije el tipo de usuario 👇",
    font=("Times New Roman", 12),
    style="success.TLabel",  # Usa un estilo que tenga un fondo verde claro
).pack(pady=40)

# Botón Administrador
tb.Button(
    ventana,
    text="Administrador",
    width=20,
    bootstyle = "outline-primary", # Estilo del botón 
    command=abrir_login_admin
).pack(pady=5)

# Botón Empleado
tb.Button(
    ventana,                          # Ventana donde se mostrará el botón
    text="Empleado",                 # Texto que aparecerá en el botón
    width=20,                        # Ancho del botón (en caracteres, no píxeles)
    bootstyle = "outline-primary", # Estilo del botón 
    command=abrir_login_empleado     # Función que se ejecuta cuando haces clic en el botón
).pack(pady=5) 

ventana.mainloop()

