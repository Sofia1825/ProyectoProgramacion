import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

# Datos del programa 
registro_agua = []  # Lista para almacenar el historial de consumo
meta_diaria = 8     # Meta diaria de vasos de agua

# Función para buscar si ya hay registro del día
def buscar_dia(fecha):
    for i in range(len(registro_agua)):
        if registro_agua[i]['fecha'] == fecha:
            return i
    return -1

# Función para agregar agua
def agregar_agua():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    try:
        vasos = simpledialog.askinteger("Agregar agua", "¿Cuántos vasos de agua tomaste hoy?")
        if vasos is None:
            return
        if vasos < 0:
            messagebox.showwarning("Error", "No puedes ingresar un número negativo.")
            return
        
        pos = buscar_dia(fecha_hoy)
        if pos != -1:
            registro_agua[pos]['vasos'].append(vasos)  # Agregar a la lista de vasos del día
        else:
            registro_agua.append({'fecha': fecha_hoy, 'vasos': [vasos]})  # Crear nuevo registro

        total = sum(registro_agua[buscar_dia(fecha_hoy)]['vasos'])  # Calcular total de vasos
        if total >= meta_diaria:
            messagebox.showinfo("¡Bien hecho!", f"Has tomado {total} vasos. ¡Meta alcanzada!")
        else:
            messagebox.showinfo("¡Vamos bien!", f"Has tomado {total} vasos hoy. Sigue así.")
    except:
        messagebox.showwarning("Error", "Por favor, ingresa un número válido.")

# Función para ver progreso de un día específico
def ver_progreso():
    fecha = simpledialog.askstring("Ver progreso", "Escribe la fecha (AAAA-MM-DD):")
    if not fecha:
        return
    pos = buscar_dia(fecha)
    if pos != -1:
        vasos = sum(registro_agua[pos]['vasos'])  # Calcular total de vasos para la fecha
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
            registro_agua[pos]['vasos'] = []  # Reiniciar la lista de vasos
            messagebox.showinfo("Reiniciado", f"Se reinició el registro del día {fecha}.")
    else:
        messagebox.showinfo("Sin registro", "No hay registro para esa fecha.")

# Crear ventana principal
root = tk.Tk()
root.title("Mi Botella de Agua")
root.geometry("300x350")

# Título
titulo = tk.Label(root, text="Mi Botella de Agua", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Botones
btn_agregar = tk.Button(root, text="Agregar vasos de agua", width=25, command=agregar_agua)
btn_agregar.pack(pady=5)

btn_progreso = tk.Button(root, text="Ver progreso de un día", width=25, command=ver_progreso)
btn_progreso.pack(pady=5)

btn_historial = tk.Button(root, text="Ver historial completo", width=25, command=ver_historial)
btn_historial.pack(pady=5)

btn_reiniciar = tk.Button(root, text="Reiniciar un día", width=25, command=reiniciar_dia)
btn_reiniciar.pack(pady=5)

btn_salir = tk.Button(root, text="Salir", width=25, command=root.destroy)
btn_salir.pack(pady=20)

# Iniciar la aplicación
root.mainloop()
