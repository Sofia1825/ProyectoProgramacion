#Proyecto Final Programacion 1. Sofia Vanegas Reyes, Ashly Bolaños Calambas

import tkinter as tk #Se importa el módulo gráfico Tkinter como tk para crear interfaces gráficas.
from tkinter import messagebox, simpledialog #e importan para mostrar mensajes emergentes y pedir datos al usuario.
from datetime import datetime, timedelta #Permiten manejar fechas y tiempos.
import matplotlib.pyplot as plt #Se usa para graficar el consumo de agua.

# Datos del programa
registro_agua = [] # Lista que guarda los registros diarios de consumo de agua.
meta_diaria = 8  # Meta diaria predeterminada: 8 vasos.

# Función para buscar si ya hay registro del día
def buscar_dia(fecha):
    for i in range(len(registro_agua)): # Recorre todos los registros guardados
        if registro_agua[i]['fecha'] == fecha: ## Compara si la fecha ya fue registrada
            return i # Devuelve el índice si la encuentra
    return -1 # Si no la encuentra, devuelve -1

# Función para actualizar el estado del progreso diario
def actualizar_estado():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d") # Obtiene la fecha actual
    pos = buscar_dia(fecha_hoy) # Verifica si hay registro para hoy
    total = sum(registro_agua[pos]['vasos']) if pos != -1 else 0 # Suma total de vasos hoy si existe el registro
# Actualiza etiqueta visual según progreso    
    if total >= meta_diaria: 
        lbl_estado.config(text=f" Meta alcanzada ({total}/{meta_diaria})", fg="green")
    else:
        lbl_estado.config(text=f" Progreso: {total}/{meta_diaria} vasos", fg="blue")

# Función para agregar vasos agua
def agregar_agua():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d") # Fecha actual
    try:
        vasos = simpledialog.askinteger("Agregar agua", "¿Cuántos vasos de agua tomaste hoy?") # Solicita cantidad
    # Si el usuario cancela
        if vasos is None: 
            return
        if vasos < 0:
            messagebox.showwarning("Error", "No puedes ingresar un número negativo.")
            return
    #Valida que el número ingresado sea correcto (positivo y no nulo). 
        pos = buscar_dia(fecha_hoy)
        if pos != -1:
            registro_agua[pos]['vasos'].append(vasos) # Si ya hay registro, agrega más vasos
        else:
            registro_agua.append({'fecha': fecha_hoy, 'vasos': [vasos]}) # Si no hay, crea nuevo registro

        total = sum(registro_agua[buscar_dia(fecha_hoy)]['vasos']) # Recalcula el total
        actualizar_estado() # Refresca estado visual
    # Muestra mensaje motivacional     
        if total >= meta_diaria:
            messagebox.showinfo("¡Bien hecho!", f"Has tomado {total} vasos. ¡Meta alcanzada!")
        else:
            messagebox.showinfo("¡Vamos bien!", f"Has tomado {total} vasos hoy. Sigue así.")
    except:
        messagebox.showwarning("Error", "Por favor, ingresa un número válido.") # Captura errores

# Función para cambiar la meta diaria
def cambiar_meta():
    global meta_diaria  # Permite modificar variable global
    nueva_meta = simpledialog.askinteger("Cambiar meta", "¿Cuál es tu nueva meta diaria (vasos)?")
    if nueva_meta is not None:
        if nueva_meta > 0:
            meta_diaria = nueva_meta
            actualizar_estado() # Refresca estado visual
            messagebox.showinfo("Meta actualizada", f"La nueva meta diaria es {meta_diaria} vasos.")
        else:
            messagebox.showwarning("Error", "La meta debe ser un número positivo.")

# Función para ver progreso de un día específico
def ver_progreso():
    fecha = simpledialog.askstring("Ver progreso", "Escribe la fecha (AAAA-MM-DD):")
    if not fecha:
        return # Si se cancela
    pos = buscar_dia(fecha)
    if pos != -1:
        vasos = sum(registro_agua[pos]['vasos'])
        if vasos >= meta_diaria:
            messagebox.showinfo("Progreso", f"En {fecha} tomaste {vasos} vasos. ¡Meta alcanzada!")
        else:
            messagebox.showinfo("Progreso", f"En {fecha} tomaste {vasos} vasos. ¡Puedes mejorar!")
    else:
        messagebox.showinfo("Progreso", "No hay registro para esa fecha.")

# Función para ver historial completo
def ver_historial():
    if not registro_agua:
        messagebox.showinfo("Historial", "No hay registros aún.")
        return
    historial = "\n".join([f"{fila['fecha']}: {sum(fila['vasos'])} vasos (Detalles: {fila['vasos']})" for fila in registro_agua])
    messagebox.showinfo("Historial de consumo", historial)

# Función para reiniciar un día
def reiniciar_dia():
    fecha = simpledialog.askstring("Reiniciar día", "Escribe la fecha (AAAA-MM-DD):")
    if not fecha:
        return
    pos = buscar_dia(fecha)
    if pos != -1:
        confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que quieres reiniciar el día {fecha}?")
        if confirmar:
            registro_agua[pos]['vasos'] = [] # Limpia lista de vasos
            actualizar_estado()
            messagebox.showinfo("Reiniciado", f"Se reinició el registro del día {fecha}.")
    else:
        messagebox.showinfo("Sin registro", "No hay registro para esa fecha.")

# Función para mostrar gráfico de consumo
def mostrar_grafico():
    if not registro_agua:
        messagebox.showinfo("Gráfico", "No hay datos suficientes para mostrar el gráfico.")
        return

    fechas = []
    valores = []

    hoy = datetime.now()
    for i in range(6, -1, -1):  # Últimos 7 días
        dia = (hoy - timedelta(days=i)).strftime("%Y-%m-%d")
        pos = buscar_dia(dia)
        fechas.append(dia)
        valores.append(sum(registro_agua[pos]['vasos']) if pos != -1 else 0)

    plt.figure(figsize=(8, 4))
    plt.bar(fechas, valores, color='#64b5f6') # Barra azul por día
    plt.axhline(y=meta_diaria, color='green', linestyle='--', label='Meta diaria')
    plt.xticks(rotation=45)
    plt.ylabel("Vasos de agua")
    plt.title("Consumo de agua (últimos 7 días)")
    plt.legend()
    plt.tight_layout()
    plt.show()

# Crear ventana principal
root = tk.Tk()
root.title("Mi Botella de Agua")
root.geometry("360x500")
root.config(bg="#e3f2fd") # Fondo azul claro

#Estilo de botones
estilo_boton = {
    "font": ("Arial", 12),
    "bg": "#64b5f6",
    "fg": "white",
    "activebackground": "#42a5f5",
    "activeforeground": "white",
    "relief": "flat",
    "width": 25,
    "height": 2
}

# Título e indicador de estado
titulo = tk.Label(root, text="💧 Mi Botella de Agua 💧", font=("Arial", 18, "bold"), bg="#e3f2fd", fg="#0d47a1")
titulo.pack(pady=15)

# Indicador visual de progreso
lbl_estado = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#e3f2fd")
lbl_estado.pack(pady=5)
actualizar_estado()

# Botones
tk.Button(root, text="Agregar vasos de agua", command=agregar_agua, **estilo_boton).pack(pady=5)
tk.Button(root, text="Ver progreso de un día", command=ver_progreso, **estilo_boton).pack(pady=5)
tk.Button(root, text="Ver historial completo", command=ver_historial, **estilo_boton).pack(pady=5)
tk.Button(root, text="Cambiar meta diaria", command=cambiar_meta, **estilo_boton).pack(pady=5)
tk.Button(root, text="Ver gráfico semanal", command=mostrar_grafico, **estilo_boton).pack(pady=5)
tk.Button(root, text="Reiniciar un día", command=reiniciar_dia, **estilo_boton).pack(pady=5)
tk.Button(root, text="Salir", command=root.destroy, **estilo_boton).pack(pady=20)

# Footer
tk.Label(root, text="¡Mantente hidratado!", font=("Arial", 10, "italic"), bg="#e3f2fd", fg="#1e88e5").pack(side="bottom", pady=10)

# Iniciar app
root.mainloop()
