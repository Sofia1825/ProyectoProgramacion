# Mi Botella de Agua (versión con matrices) sin interfaz
# Proyecto Final - Programación I

from datetime import datetime

# Lista de listas: cada sublista contiene [fecha, vasos]
registro_agua = []
meta_diaria = 8

# Función para mostrar el menú
def mostrar_menu():
    print("\n--- MI BOTELLA DE AGUA ---")
    print("1. Agregar vasos de agua de hoy")
    print("2. Ver progreso de un día")
    print("3. Ver historial completo")
    print("4. Reiniciar un día")
    print("5. Salir")

# Función para buscar si ya hay registro del día
def buscar_dia(fecha):
    for i in range(len(registro_agua)):
        if registro_agua[i][0] == fecha:
            return i
    return -1

# Función para agregar agua
def agregar_agua():
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    try:
        vasos = int(input("¿Cuántos vasos de agua tomaste hoy? "))
        if vasos < 0:
            print("No puedes ingresar un número negativo.")
            return
        pos = buscar_dia(fecha_hoy)
        if pos != -1:
            registro_agua[pos][1] += vasos
        else:
            registro_agua.append([fecha_hoy, vasos])
        print(f"¡Genial! Has registrado {vasos} vasos para hoy.")

        if registro_agua[buscar_dia(fecha_hoy)][1] >= meta_diaria:
            print("¡Felicidades! Alcanzaste tu meta de hoy.")
        else:
            print("¡Sigue así! Estás haciendo un gran trabajo.")
    except ValueError:
        print("Por favor, ingresa un número válido.")

# Función para ver el progreso de un día específico
def ver_progreso():
    fecha = input("Escribe la fecha (AAAA-MM-DD): ")
    pos = buscar_dia(fecha)
    if pos != -1:
        vasos = registro_agua[pos][1]
        print(f"En {fecha} tomaste {vasos} vasos de agua.")
        if vasos >= meta_diaria:
            print("¡Meta alcanzada ese día!")
        else:
            print("No alcanzaste la meta ese día. ¡A mejorar!")
    else:
        print("No hay registro de esa fecha.")

# Función para mostrar historial completo
def ver_historial():
    if not registro_agua:
        print("No hay registros aún.")
    else:
        print("\n--- Historial de consumo ---")
        for fila in registro_agua:
            print(f"{fila[0]}: {fila[1]} vasos")

# Función para reiniciar un día
def reiniciar_dia():
    fecha = input("Escribe la fecha que quieres reiniciar (AAAA-MM-DD): ")
    pos = buscar_dia(fecha)
    if pos != -1:
        confirmar = input(f"¿Seguro que quieres reiniciar el día {fecha}? (s/n): ").lower()
        if confirmar == "s":
            registro_agua[pos][1] = 0
            print("Día reiniciado con éxito.")
        else:
            print("No se reinició el registro.")
    else:
        print("No hay registro para esa fecha.")

# Programa principal
while True:
    mostrar_menu()
    opcion = input("Selecciona una opción (1-5): ")

    if opcion == "1":
        agregar_agua()
    elif opcion == "2":
        ver_progreso()
    elif opcion == "3":
        ver_historial()
    elif opcion == "4":
        reiniciar_dia()
    elif opcion == "5":
        print("Gracias por usar Mi Botella de Agua. ¡Hasta pronto!")
        break
    else:
        print("Opción no válida. Intenta de nuevo.")

