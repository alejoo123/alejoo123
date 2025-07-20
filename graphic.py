import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.style import Bootstyle
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.dialogs import Messagebox
import re
import os
from conexion_db import verificar_usuario_en_bd
import smtplib
import random
from email.mime.text import MIMEText
from collections import Counter
from  class_up import *
import tkinter as tk
from tkinter import messagebox
from class_up import ComandoAgregarEmpleado, ComandoEliminarEmpleado, ComandoVerHistoricoVentas






#Empleado en sesion
#Variable para almacenar el empleado en sesion
# None se asigna al iniciar sesion, Luego se asigna al iniciar sesion
#Se usa para veriicar si un empleado esta en sesion o no
empleado_en_sesion = None

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
# Precios por ciudad
# Diccionario que contiene los precios por ciudad
CIUDADES_PRECIOS = {
    "Bahía de Caráquez": {"precio": 5.50, "tiempo": "45 min"},
    "Portoviejo": {"precio": 3.50, "tiempo": "30 min"},
    "Chone": {"precio": 4.75, "tiempo": "1h 10min"},
    "Pedernales": {"precio": 6.25, "tiempo": "1h 30min"},
    "Jipijapa": {"precio": 3.25, "tiempo": "50 min"},
    "Montecristi": {"precio": 3.75, "tiempo": "40 min"},
    "San Jacinto": {"precio": 2.50, "tiempo": "20 min"}
}
MODERN_STYLE = {
    "primary": "#4e73df",
    "secondary": "#858796",
    "success": "#1cc88a",
    "info": "#36b9cc",
    "warning": "#f6c23e",
    "danger": "#e74a3b",
    "light": "#f8f9fc",
    "dark": "#5a5c69"
}

def verificar_estructura_tabla():
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'usuarios'
            ORDER BY ordinal_position
        """)
        columnas = cursor.fetchall()
        print("Estructura de la tabla usuarios:")
        for col in columnas:
            print(f"{col[0]} ({col[1]})")
    finally:
        conn.close()

verificar_estructura_tabla()






    
def verificar_credenciales(usuario, clave, ventana_login):
    datos_usuario = verificar_usuario_en_bd(usuario, clave)
    if datos_usuario and datos_usuario["rol"] == "admin":
        global ADMIN
        ADMIN = Empleado(
            cedula=datos_usuario["id"],
            nombre=datos_usuario["nombre"],
            apellido=datos_usuario["apellido"],
            correo_electronico=datos_usuario["correo"],
            edad=0,  # Valor por defecto
            codigo=0,  # Valor por defecto
            ubicacion="Oficina",  # Valor por defecto
            clave=datos_usuario["clave"]
        )
        messagebox.showinfo("Acceso concedido", "✅ Ingresaste como administrador.")
        interfaz_admin(ventana_login)
    else:
        messagebox.showerror("Error", "❌ Credenciales incorrectas o no eres administrador.")

        
def verificar_credenciales_empe(usuario, clave, ventana_empleado):
    datos_usuario = verificar_usuario_en_bd(usuario, clave)
    if datos_usuario and datos_usuario["rol"] == "empleado":
        global empleado_en_sesion
        empleado_en_sesion = Empleado(0, datos_usuario["nombre"], datos_usuario["apellido"],
                                      datos_usuario["correo"], 0, 0, "Terminal", clave)
        messagebox.showinfo("Acceso concedido", "✅ Ingresaste como empleado.")
        interfaz_empleado(ventana_empleado)
    else:
        messagebox.showerror("Error", "❌ Credenciales incorrectas o no eres empleado.")






def interfaz_admin(ventana_login):
    
    ventana_login.withdraw()
    
    ventana_admin = tb.Window(title="Panel de Administrador", themename="litera")
    ventana_admin.geometry("1200x800")
    
    # Frame principal
    main_frame = tb.Frame(ventana_admin)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Lista de empleados
    empleados = Empleado.get_all()
    
    # Tabla de empleados
    columns = [
        {"text": "Cédula", "stretch": False},
        {"text": "Nombre"},
        {"text": "Apellido"},
        {"text": "Ubicación"},
        {"text": "Código", "stretch": False},
        {"text": "Acciones", "stretch": False}
    ]
    
    rowdata = [
        (
            emp._cedula,
            emp.nombre,
            emp.apellido,
            emp._ubicacion,
            emp.codigo,
            f"Eliminar|Editar"
        ) for emp in empleados
    ]
    
    table = Tableview(
        master=main_frame,
        coldata=columns,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle="primary"
    )
    table.pack(fill="both", expand=True, pady=10)
    
    # Botones de acción
    btn_frame = tb.Frame(main_frame)
    btn_frame.pack(fill="x", pady=10)
    
    btn_agregar = tb.Button(
        btn_frame,
        text="Agregar Empleado",
        bootstyle="success",
        command=lambda: abrir_formulario_empleado()
    )
    btn_agregar.pack(side="left", padx=5)
    
    btn_ventas = tb.Button(
        btn_frame,
        text="Ver Histórico Ventas",
        bootstyle="info",
        command=lambda: ComandoVerHistoricoVentas(ADMIN).ejecutar()
    )
    btn_ventas.pack(side="left", padx=5)
    
    def abrir_formulario_empleado():
        form = tb.Toplevel(title="Nuevo Empleado")
        form.geometry("500x600")
        
        # Definimos los campos con nombres que coincidan con la base de datos
        campos = [
        ("Cédula", "cedula"),
        ("Nombre", "nombre"), 
        ("Apellido", "apellido"),
        ("Correo electrónico", "correo"),  # Usamos 'correo' que es más simple
        ("Edad", "edad"),
        ("Código", "codigo"),
        ("Ubicación", "ubicacion"),
        ("Clave", "clave")
    ]
        
        entries = {}
        for text, field in campos:
            frame = tb.Frame(form)
            frame.pack(fill="x", padx=10, pady=5)
            tb.Label(frame, text=text).pack(side="left")
            entry = tb.Entry(frame)
            entry.pack(side="right", fill="x", expand=True)
            entries[field] = entry
        
        def guardar():
            data = {k: v.get() for k, v in entries.items()}
            # Convertimos la edad a número
            try:
                data['edad'] = int(data['edad'])
            except ValueError:
                Messagebox.show_error("La edad debe ser un número", "Error")
                return
            
            comando = ComandoAgregarEmpleado(ADMIN, data)
            success, msg = comando.ejecutar()
            
            if success:
                Messagebox.show_info(msg, "Éxito")
                form.destroy()
                # Refrescamos la interfaz
                ventana_admin.destroy()
                interfaz_admin(ventana_login)
            else:
                Messagebox.show_error(msg, "Error")
        
        tb.Button(form, text="Guardar", command=guardar).pack(pady=20)
    ventana_admin.mainloop()
        
        
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

    
def abrir_ventana_auditoria(lista):
    
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
        command = lambda: agregar_empleado_command(lista)
    ).pack(pady=5)
    
    def eliminar_empleado_command():
        # Ejemplo: elimina el primer empleado de la lista
        if empleados_registrados:
            comando = ComandoEliminarEmpleado(ADMIN, empleados_registrados[0])
            comando.ejecutar()
            messagebox.showinfo("Auditoria", "Empleado eliminado.")
        else:
            messagebox.showwarning("Auditoria", "No hay empleados para eliminar.")

    #boton3 Eliminar Empleado (solo registro de accion)
    tb.Button(
        frame_fondo, 
        text="Eliminar empleado", 
        bootstyle="outline-primary", 
        command= eliminar_empleado_command
    ).pack(pady=10)
    
    def ver_historico_ventas_command():
        comando = ComandoVerHistoricoVentas(ADMIN)
        comando.ejecutar()
        
    #boton4 Ver historico de ventas
    tb.Button(
        frame_fondo, 
        text= "Ver historico de ventas", 
        bootstyle="outline-primary", 
        command = ver_historico_ventas_command
        ).pack(pady=10)

def agregar_empleado_command(lista_empleados):
    ventana_nuevo = tb.Toplevel()
    ventana_nuevo.title("Agregar nuevo empleado")
    ventana_nuevo.geometry("600x600")

    campos = [
        ("ID", "id"),
        ("Nombre", "nombre"),
        ("Apellido", "apellido"),
        ("Correo electrónico", "correo"),
        ("Edad", "edad"),
        ("Ubicación", "ubicacion"),
        ("Clave", "clave")
    ]
    entradas = {}

    for texto, clave in campos:
        tb.Label(ventana_nuevo, text=texto).pack(pady=5)
        entrada = tb.Entry(ventana_nuevo)
        entrada.pack()
        entradas[clave] = entrada

    def guardar_empleado():
        try:
            id_empleado = int(entradas["id"].get())
            nombre = entradas["nombre"].get()
            apellido = entradas["apellido"].get()
            correo = entradas["correo"].get()
            edad = int(entradas["edad"].get())
            ubicacion = entradas["ubicacion"].get()
            clave = entradas["clave"].get()
            if not (nombre and apellido and correo and ubicacion and clave):
                messagebox.showwarning("Campos vacíos", "Completa todos los campos.")
                return
        except Exception:
            messagebox.showerror("Error", "Datos inválidos.")
            return

        nuevo_empleado = Empleado(id_empleado, nombre, apellido, correo, edad, 0, ubicacion, clave)
        empleados_registrados.append(nuevo_empleado)
        comando = ComandoAgregarEmpleado(ADMIN, nuevo_empleado)
        comando.ejecutar()
        lista_empleados.insert(tk.END, f"{nombre} {apellido} - {ubicacion}")  # Actualiza la lista visual
        messagebox.showinfo("Auditoria", f"Empleado {nombre} agregado correctamente.")
        ventana_nuevo.destroy()

    tb.Button(ventana_nuevo, text="Guardar", command=guardar_empleado).pack(pady=20)
    
    
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
    ventana_sesion_empleado.withdraw()
    
    # Ventana principal
    ventana_empleado = tb.Window(title=f"Bienvenido/a {empleado_en_sesion.nombre}", themename="litera")
    ventana_empleado.geometry("1200x700+100+50")
    ventana_empleado.resizable(False, False)
    
    # Configurar estilo moderno
    style = tb.Style()
    style.configure('primary.TButton', font=('Helvetica', 10, 'bold'))
    style.configure('success.TButton', font=('Helvetica', 10, 'bold'))
    style.configure('TCombobox', font=('Helvetica', 10))
    
    # Frame principal
    main_frame = tb.Frame(ventana_empleado, bootstyle="light")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Header
    header_frame = tb.Frame(main_frame)
    header_frame.pack(fill="x", pady=(0, 20))
    
    tb.Label(
        header_frame,
        text=f"🚌 Terminal de Buses - {empleado_en_sesion.ubicacion}",
        font=("Helvetica", 16, "bold"),
        bootstyle="primary"
    ).pack(side="left")
    
    tb.Button(
        header_frame,
        text="Cerrar Sesión",
        bootstyle="danger-outline",
        command=ventana_empleado.destroy
    ).pack(side="right")
    
    # Contenedor de dos columnas
    content_frame = tb.Frame(main_frame)
    content_frame.pack(fill="both", expand=True)
    
    # Columna izquierda (Formulario)
    form_frame = tb.Frame(content_frame, width=400, bootstyle="light")
    form_frame.pack(side="left", fill="y", padx=(0, 20))
    
    # Card de selección
    form_card = tb.Frame(form_frame, bootstyle="light", padding=20)
    form_card.pack(fill="both", expand=True)
    
    tb.Label(
        form_card,
        text="Generar Nuevo Boleto",
        font=("Helvetica", 14, "bold"),
        bootstyle="primary"
    ).pack(pady=(0, 20))
    
    # Selección de destino
    tb.Label(
        form_card,
        text="Ciudad Destino:",
        font=("Helvetica", 10),
        bootstyle="secondary"
    ).pack(anchor="w", pady=(10, 5))
    
    destino_combo = tb.Combobox(
        form_card,
        values=list(CIUDADES_PRECIOS.keys()),
        state="readonly",
        font=("Helvetica", 10),
        bootstyle="primary"
    )
    destino_combo.pack(fill="x", pady=(0, 15))
    destino_combo.current(0)
    
    # Info del destino seleccionado
    destino_info = tb.Label(
        form_card,
        text=f"Precio: ${CIUDADES_PRECIOS[list(CIUDADES_PRECIOS.keys())[0]]['precio']} • Tiempo: {CIUDADES_PRECIOS[list(CIUDADES_PRECIOS.keys())[0]]['tiempo']}",
        font=("Helvetica", 9),
        bootstyle="info"
    )
    destino_info.pack(anchor="w", pady=(0, 20))
    
    # Actualizar info cuando cambia la selección
    def update_destino_info(event):
        ciudad = destino_combo.get()
        info = CIUDADES_PRECIOS[ciudad]
        destino_info.config(text=f"Precio: ${info['precio']} • Tiempo: {info['tiempo']}")
    
    destino_combo.bind("<<ComboboxSelected>>", update_destino_info)
    
    # Selección de hora
    tb.Label(
        form_card,
        text="Hora de Salida:",
        font=("Helvetica", 10),
        bootstyle="secondary"
    ).pack(anchor="w", pady=(10, 5))
    
    horas_frame = tb.Frame(form_card)
    horas_frame.pack(fill="x")
    
    horas_disponibles = ["05:00", "07:00", "09:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00"]
    for i, hora in enumerate(horas_disponibles):
        btn = tb.Button(
            horas_frame,
            text=hora,
            width=6,
            bootstyle="outline-primary" if i != 0 else "primary",
            command=lambda h=hora: generar_boleto_preview(h)
        )
        btn.pack(side="left", padx=5, pady=5)
    
    # Columna derecha (Preview y acciones)
    preview_frame = tb.Frame(content_frame, bootstyle="light")
    preview_frame.pack(side="right", fill="both", expand=True)
    
    # Card de preview
    preview_card = tb.Frame(preview_frame, bootstyle="light", padding=20)
    preview_card.pack(fill="both", expand=True)
    
    tb.Label(
        preview_card,
        text="Resumen del Boleto",
        font=("Helvetica", 14, "bold"),
        bootstyle="primary"
    ).pack(pady=(0, 20))
    
    # Contenedor del preview
    boleto_preview = tb.Frame(preview_card, bootstyle="light", relief="solid", borderwidth=1)
    boleto_preview.pack(fill="both", expand=True, pady=(0, 20))
    
    # Botón de confirmación (CREADO UNA SOLA VEZ)
    confirm_btn = tb.Button(
        preview_card,
        text="Confirmar y Generar Boleto",
        bootstyle="success",
        width=25,
        state="disabled"
    )
    confirm_btn.pack(pady=10)
    
    # Función para generar el preview
    def generar_boleto_preview(hora_seleccionada):
        # Limpiar el preview anterior
        for widget in boleto_preview.winfo_children():
            widget.destroy()
        
        ciudad = destino_combo.get()
        if not ciudad:
            Messagebox.show_warning("Seleccione un destino", "Advertencia")
            return
            
        bus = random.choice(transportes_disponibles)
        precio = CIUDADES_PRECIOS[ciudad]["precio"]
        tiempo = CIUDADES_PRECIOS[ciudad]["tiempo"]
        
        # Header del boleto
        header = tb.Frame(boleto_preview, bootstyle="primary")
        header.pack(fill="x", pady=(10, 15), padx=10)
        
        tb.Label(
            header,
            text="BOLETO DE VIAJE",
            font=("Helvetica", 12, "bold"),
            bootstyle="inverse-primary"
        ).pack(pady=5)
        
        # Cuerpo del boleto
        body = tb.Frame(boleto_preview)
        body.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Datos del viaje
        viaje_frame = tb.Frame(body)
        viaje_frame.pack(fill="x", pady=5)
        
        tb.Label(
            viaje_frame,
            text="🚍 Viaje:",
            font=("Helvetica", 10, "bold"),
            bootstyle="dark"
        ).pack(side="left", anchor="w")
        
        tb.Label(
            viaje_frame,
            text=f"{empleado_en_sesion.ubicacion} → {ciudad}",
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack(side="left", padx=10)
        
        # Hora y fecha
        hora_frame = tb.Frame(body)
        hora_frame.pack(fill="x", pady=5)
        
        tb.Label(
            hora_frame,
            text="🕒 Hora:",
            font=("Helvetica", 10, "bold"),
            bootstyle="dark"
        ).pack(side="left", anchor="w")
        
        tb.Label(
            hora_frame,
            text=f"{hora_seleccionada} • {datetime.now().strftime('%d/%m/%Y')}",
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack(side="left", padx=10)
        
        # Precio
        precio_frame = tb.Frame(body)
        precio_frame.pack(fill="x", pady=5)
        
        tb.Label(
            precio_frame,
            text="💵 Precio:",
            font=("Helvetica", 10, "bold"),
            bootstyle="dark"
        ).pack(side="left", anchor="w")
        
        tb.Label(
            precio_frame,
            text=f"${precio:.2f} • Tiempo estimado: {tiempo}",
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack(side="left", padx=10)
        
        # Datos del bus
        bus_frame = tb.Frame(body)
        bus_frame.pack(fill="x", pady=5)
        
        tb.Label(
            bus_frame,
            text="🚌 Transporte:",
            font=("Helvetica", 10, "bold"),
            bootstyle="dark"
        ).pack(side="left", anchor="w")
        
        tb.Label(
            bus_frame,
            text=f"{bus['nombre']} • Disco: {bus['disco']}",
            font=("Helvetica", 10),
            bootstyle="secondary"
        ).pack(side="left", padx=10)
        
        # Habilitar y actualizar el botón de confirmación
        confirm_btn.config(
            command=lambda: confirmar_boleto(ciudad, hora_seleccionada, precio, bus),
            state="normal"
        )
    
    # Función para confirmar el boleto
    def confirmar_boleto(ciudad, hora, precio, bus):
        # Registrar la transacción
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        registro = (
            f"[{timestamp}] Pasajero: {empleado_en_sesion.nombre} {empleado_en_sesion.apellido} | "
            f"Destino: {ciudad} | Hora: {hora} | Bus: {bus['disco']} | "
            f"Precio: ${precio:.2f}\n"
        )
        
        with open("historico_ventas.txt", "a") as f:
            f.write(registro)
        
        # Mostrar notificación
        toast = ToastNotification(
            title="Boleto Generado",
            message=f"Boleto para {ciudad} a las {hora} generado correctamente!",
            duration=3000,
            bootstyle="success"
        )
        toast.show_toast()
        
        # Actualizar vista
        generar_boleto_preview(hora)
    
    # Inicializar con un preview por defecto
    generar_boleto_preview(horas_disponibles[0])
    
    ventana_empleado.mainloop()





    
    
    
    
    
    
    
    
    
    
    
    




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

