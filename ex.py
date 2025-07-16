import re
print("     _||_")
print("    |    |")
print("   _|____|_")
print("  |        |")
print("  |  HOTEL |")
print(" _|________|_")
print("|  __   __   |")
print("| |__| |__|  |")
print("| |__| |__|  |")
print("|____________|")
print("================")
print("Bienvenido al Hotel Buen Descanso")
print("================")
print("1. Registra huesped")
print("2. Realizar reserva")
print("3. Registrar Ingreso (Check-In)")
print("4. Registrar salid (Check-Out)")
print("5. Administraciòn (Acceso restrigindo)")
print("6. Salir")

patron=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


mi_variable = input("Selecciona una opcion:")
print(mi_variable)


def registrarHuesped(nombre_usuario,apellido_usuario,documento_de_identidad,correo_electronico,numero_de_telefono):
    if(len(nombre_usuario ) >= 3): 
        return "El nombre es correcto"

    if(len(apellido_usuario) >=3):
        return "El apellido es correcto"

    if(len(documento_de_identidad)>3 and len(documento_de_identidad)<15):
        return "Documento de identidad es correcto"

    if(correo_electronico):
        if(re.match(patron,correo_electronico)):
            return " correo electronico es correcto"

    if(len(numero_de_telefono)>=7 and len (numero_de_telefono)<=15):
        return " El numero de telefono es correcto"
    
    return "Todo esta bien"




if (mi_variable == "1"):
    nombre_usuario = input("Nombre")
    apellido_usuario = input("apellido")
    documento_de_identidad = int(input("documento de identidad"))
    correo_electronico = input("correo electronico")
    numero_de_telefono = int(input("Numero de telefono"))
    registrarHuesped(nombre_usuario, apellido_usuario, documento_de_identidad, correo_electronico, numero_de_telefono)

import csv
import os

ARCHIVO_HABITACIONES = "data/habitaciones.csv"

# Inicializa archivo si no existe
def inicializar_archivo_habitaciones():
    if not os.path.exists(ARCHIVO_HABITACIONES):
        with open(ARCHIVO_HABITACIONES, mode='w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["numero", "tipo", "precio", "estado"])

def precio_por_tipo(tipo):
    if tipo.lower() == "estándar":
        return 120000
    elif tipo.lower() == "suite":
        return 250000
    return 0

def validar_tipo(tipo):
    return tipo.lower() in ["estándar", "suite"]

def numero_habitacion_existe(numero):
    with open(ARCHIVO_HABITACIONES, mode='r') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            if fila["numero"] == numero:
                return True
    return False

def registrar_habitacion():
    print("\n=== Registro de Habitación ===")
    numero = input("Número de habitación: ").strip()

    if numero_habitacion_existe(numero):
        print("❌ Ya existe una habitación con ese número.")
        return

    tipo = input("Tipo de habitación (Estándar o Suite): ").strip().capitalize()
    if not validar_tipo(tipo):
        print("❌ Tipo no válido. Debe ser 'Estándar' o 'Suite'.")
        return

    precio = precio_por_tipo(tipo)
    estado = "Disponible"

    with open(ARCHIVO_HABITACIONES, mode='a', newline='') as archivo:
        writer = csv.writer(archivo)
        writer.writerow([numero, tipo, precio, estado])

    print("✅ Habitación registrada exitosamente.")

def mostrar_habitaciones():
    print("\n=== Lista de Habitaciones ===")
    with open(ARCHIVO_HABITACIONES, mode='r') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            print(f"Habitación {fila['numero']} | Tipo: {fila['tipo']} | Precio: ${fila['precio']} | Estado: {fila['estado']}")

# Inicializar archivo al ejecutar
inicializar_archivo_habitaciones()


import csv
import os
from datetime import datetime

ARCHIVO_RESERVAS = "data/reservas.csv"
ARCHIVO_HABITACIONES = "data/habitaciones.csv"

def cargar_reservas_activas():
    reservas = []
    with open(ARCHIVO_RESERVAS, mode='r') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            reservas.append(fila)
    return reservas

def actualizar_estado_habitacion(numero, nuevo_estado):
    filas = []
    with open(ARCHIVO_HABITACIONES, mode='r') as archivo:
        reader = csv.DictReader(archivo)
        filas = list(reader)

    with open(ARCHIVO_HABITACIONES, mode='w', newline='') as archivo:
        fieldnames = ["numero", "tipo", "precio", "estado"]
        writer = csv.DictWriter(archivo, fieldnames=fieldnames)
        writer.writeheader()
        for fila in filas:
            if fila["numero"] == numero:
                fila["estado"] = nuevo_estado
            writer.writerow(fila)

def registrar_salida():
    print("\n=== Registro de Salida (Check-Out) ===")
    documento = input("Documento del huésped: ").strip()

    reservas = cargar_reservas_activas()
    reserva_encontrada = None
    for reserva in reservas:
        if reserva["documento_huesped"] == documento:
            reserva_encontrada = reserva
            break

    if not reserva_encontrada:
        print("❌ No se encontró una reserva activa para este documento.")
        return

    fecha_ingreso = datetime.strptime(reserva_encontrada["fecha_ingreso"], "%Y-%m-%d")
    fecha_actual = datetime.now()
    noches_real = (fecha_actual - fecha_ingreso).days
    if noches_real < 1:
        noches_real = 1  # mínimo 1 noche

    tipo = reserva_encontrada["tipo_habitacion"]
    precio = 120000 if tipo.lower() == "estándar" else 250000
    total = noches_real * precio

    # Generar factura
    print("\n=== Factura ===")
    print(f"Nombre del huésped: {reserva_encontrada['nombre']}")
    print(f"Documento: {reserva_encontrada['documento_huesped']}")
    print(f"Tipo de habitación: {tipo}")
    print(f"Número de habitación: {reserva_encontrada['numero_habitacion']}")
    print(f"Fecha de ingreso: {reserva_encontrada['fecha_ingreso']}")
    print(f"Fecha de salida: {fecha_actual.strftime('%Y-%m-%d')}")
    print(f"Número de noches: {noches_real}")
    print(f"Total a pagar: ${total:,}")

    # Cambiar habitación a disponible
    actualizar_estado_habitacion(reserva_encontrada["numero_habitacion"], "Disponible")

    # Eliminar reserva del archivo
    with open(ARCHIVO_RESERVAS, mode='r') as archivo:
        reservas = list(csv.DictReader(archivo))

    with open(ARCHIVO_RESERVAS, mode='w', newline='') as archivo:
        fieldnames = ["documento_huesped", "nombre", "tipo_habitacion", "numero_habitacion",
                      "fecha_ingreso", "fecha_salida", "noches", "costo"]
        writer = csv.DictWriter(archivo, fieldnames=fieldnames)
        writer.writeheader()
        for r in reservas:
            if r["documento_huesped"] != documento:
                writer.writerow(r)

    print("\n✅ Check-out realizado con éxito.")

    import pandas as pd
import os

ARCHIVO_USUARIOS = "data/usuarios.txt"
ARCHIVO_HUESPEDES = "data/huespedes.csv"
ARCHIVO_HABITACIONES = "data/habitaciones.csv"
ARCHIVO_RESERVAS = "data/reservas.csv"

def cargar_usuarios():
    usuarios = {}
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as f:
            for linea in f:
                user, pwd = linea.strip().split(",")
                usuarios[user] = pwd
    return usuarios

def login_admin():
    print("\n=== Ingreso Administrador ===")
    usuarios = cargar_usuarios()
    usuario = input("usuario: ")
    clave = input("clave: ")

    if usuario in usuarios and usuarios[usuario] == clave:
        print("✅ Acceso concedido.")
        return True
    else:
        print("❌ Acceso denegado.")
        return False

def generar_reportes():
    print("\n=== Reportes Administrativos ===")

    df_huespedes = pd.read_csv(ARCHIVO_HUESPEDES)
    df_habitaciones = pd.read_csv(ARCHIVO_HABITACIONES)
    df_reservas = pd.read_csv(ARCHIVO_RESERVAS)

    print(f"👥 Total de huéspedes registrados: {len(df_huespedes)}")

    ocupadas = df_habitaciones[df_habitaciones["estado"] == "Ocupada"]
    disponibles = df_habitaciones[df_habitaciones["estado"] == "Disponible"]
    print(f"🛏️ Habitaciones ocupadas: {len(ocupadas)}")
    print(f"🛏️ Habitaciones disponibles: {len(disponibles)}")

    df_reservas["costo"] = pd.to_numeric(df_reservas["costo"], errors="coerce").fillna(0)
    ingresos_totales = df_reservas["costo"].sum()
    print(f"💰 Total ingresos por reservas: ${ingresos_totales:,.0f}")

    df_reservas["noches"] = pd.to_numeric(df_reservas["noches"], errors="coerce")
    promedio_estancia = df_reservas["noches"].mean()
    print(f"📈 Tiempo promedio de estancia: {promedio_estancia:.2f} noches")

    print("\n📋 Lista de huéspedes con historial de reservas:")
    print(df_reservas[["nombre", "documento_huesped", "noches"]])

    # Handle case where df_reservas is empty or 'noches' column is all NaN
    if not df_reservas.empty and df_reservas["noches"].dropna().empty is False:
        # Huésped con más noches
        top_huesped = df_reservas.loc[df_reservas["noches"].idxmax()]
        print(f"\n🏆 Huésped con más noches: {top_huesped['nombre']} ({top_huesped['noches']} noches)")

        # Huésped con menos noches
        low_huesped = df_reservas.loc[df_reservas["noches"].idxmin()]
        print(f"🔽 Huésped con menos noches: {low_huesped['nombre']} ({low_huesped['noches']} noches)")
    else:
        print("\nNo hay datos de reservas con noches válidas para determinar el huésped con más/menos noches.")


def menu_administracion():
    if login_admin():
        generar_reportes()
    else:
        print("❌ Usuario no autorizado.")

pip install matplotlib

import pandas as pd
import matplotlib.pyplot as plt

ARCHIVO_HABITACIONES = "data/habitaciones.csv"
ARCHIVO_RESERVAS = "data/reservas.csv"

def graficos_hotel():
    print("\n=== Generando Gráficos con Matplotlib ===")
    df_h = pd.read_csv(ARCHIVO_HABITACIONES)
    df_r = pd.read_csv(ARCHIVO_RESERVAS)

    df_r["noches"] = pd.to_numeric(df_r["noches"], errors="coerce").fillna(0)
    df_r["costo"] = pd.to_numeric(df_r["costo"], errors="coerce").fillna(0)

    # 1. Gráfica de barras: habitaciones ocupadas por tipo
    ocupadas = df_h[df_h["estado"] == "Ocupada"]
    if not ocupadas.empty:
        tipo_ocupadas = ocupadas["tipo"].value_counts()
        tipo_ocupadas.plot(kind="bar", title="Habitaciones Ocupadas por Tipo")
        plt.xlabel("Tipo de habitación")
        plt.ylabel("Cantidad")
        plt.tight_layout()
        plt.show()
    else:
        print("No hay habitaciones ocupadas para mostrar en la gráfica de barras.")


    # 2. Gráfica circular: ocupadas vs disponibles
    estados = df_h["estado"].value_counts()
    if not estados.empty:
        estados.plot(kind="pie", autopct="%1.1f%%", title="Distribución Ocupadas vs Disponibles")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos de estado de habitaciones para mostrar en la gráfica circular.")


    # 3. Gráfica de líneas: evolución de check-outs
    df_r["fecha_salida"] = pd.to_datetime(df_r["fecha_salida"], errors="coerce")
    checkouts_por_dia = df_r["fecha_salida"].value_counts().sort_index()
    if not checkouts_por_dia.empty:
        checkouts_por_dia.plot(kind="line", marker="o", title="Check-Outs por Día")
        plt.xlabel("Fecha")
        plt.ylabel("Cantidad")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos de check-outs para mostrar en la gráfica de líneas.")


    # 4. Gráfica de barras horizontal: top 10 noches hospedadas
    if not df_r.empty and df_r["noches"].sum() > 0:
        top10 = df_r.groupby("nombre")["noches"].sum().sort_values(ascending=False).head(10)
        if not top10.empty:
            top10.plot(kind="barh", title="Top 10 Huéspedes por Noches Hospedadas", color='orange')
            plt.xlabel("Noches")
            plt.tight_layout()
            plt.show()
        else:
             print("No hay datos de noches hospedadas para mostrar en la gráfica de barras horizontal.")
    else:
        print("No hay datos de reservas con noches hospedadas para mostrar en la gráfica de barras horizontal.")


    # 5. Gráfica de dispersión: noches vs valor pagado
    if not df_r.empty and df_r["noches"].sum() > 0 and df_r["costo"].sum() > 0:
        plt.scatter(df_r["noches"], df_r["costo"], alpha=0.7)
        plt.title("Relación Noches vs Costo Pagado")
        plt.xlabel("Noches")
        plt.ylabel("Costo Total")
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos de noches o costo pagado para mostrar en la gráfica de dispersión.")


    # 6. Gráfica de pastel: ingresos por tipo de habitación
    if not df_r.empty and df_r["costo"].sum() > 0:
        ingresos_tipo = df_r.groupby("tipo_habitacion")["costo"].sum()
        if not ingresos_tipo.empty:
            ingresos_tipo.plot(kind="pie", autopct="%1.1f%%", title="Ingresos por Tipo de Habitación")
            plt.ylabel("")
            plt.tight_layout()
            plt.show()
        else:
            print("No hay datos de ingresos por tipo de habitación para mostrar en la gráfica de pastel.")
    else:
        print("No hay datos de reservas con costo para mostrar en la gráfica de pastel.")


    # 7. Histograma: distribución de duración de estancias
    if not df_r.empty and df_r["noches"].sum() > 0:
        df_r["noches"].plot(kind="hist", bins=10, title="Distribución de Duración de Estancias", color="green", edgecolor="black")
        plt.xlabel("Noches")
        plt.tight_layout()
        plt.show()
    else:
        print("No hay datos de noches hospedadas para mostrar en el histograma.")


    # 8. Gráfica combinada: ingresos diarios (barras) + cantidad de huéspedes (línea)
    if not df_r.empty and (df_r["costo"].sum() > 0 or df_r["nombre"].count() > 0):
        df_r["fecha_ingreso"] = pd.to_datetime(df_r["fecha_ingreso"], errors="coerce")
        ingresos_dia = df_r.groupby("fecha_ingreso")["costo"].sum()
        huespedes_dia = df_r.groupby("fecha_ingreso")["nombre"].count()

        if not ingresos_dia.empty or not huespedes_dia.empty:
            fig, ax1 = plt.subplots()
            ingresos_dia.plot(kind="bar", ax=ax1, color="skyblue", label="Ingresos")
            ax1.set_ylabel("Ingresos ($)")
            ax1.set_xlabel("Fecha")
            ax2 = ax1.twinx()
            huespedes_dia.plot(kind="line", ax=ax2, color="red", marker="o", label="Huéspedes")
            ax2.set_ylabel("Cantidad de huéspedes")
            ax1.set_title("Ingresos y Huéspedes por Día")
            fig.autofmt_xdate()
            plt.tight_layout()
            plt.show()
        else:
            print("No hay datos de ingresos o huéspedes por día para mostrar en la gráfica combinada.")
    else:
        print("No hay datos de reservas con costo o nombre para mostrar en la gráfica combinada.")

        import os
import sys

# Importar módulos - Removed as functions are in the notebook
# from huespedes import registrar_huesped
# from habitaciones import registrar_habitacion, mostrar_habitaciones
# from reservas import realizar_reserva
# from check_out import registrar_salida
# from admin import menu_administracion
# from graficos import graficos_hotel

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\nPresiona Enter para continuar...")

def menu_principal():
    while True:
        limpiar_pantalla()
        print("""
╔════════════════════════════════════════════════════╗
║        HOTEL BUENDESCANSO - SISTEMA DE GESTIÓN     ║
╠════════════════════════════════════════════════════╣
║ 1. Registrar Huésped                               ║
║ 2. Registrar Habitación                            ║
║ 3. Realizar Reserva                                ║
║ 4. Registrar Salida (Check-Out)                    ║
║ 5. Acceder a Administración                        ║
║ 6. Ver Reportes Gráficos                           ║
║ 7. Salir del Sistema                               ║
╚════════════════════════════════════════════════════╝
""")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_huesped()
            pausar()
        elif opcion == "2":
            registrar_habitacion()
            pausar()
        elif opcion == "3":
            realizar_reserva()
            pausar()
        elif opcion == "4":
            registrar_salida()
            pausar()
        elif opcion == "5":
            menu_administracion()
            pausar()
        elif opcion == "6":
            graficos_hotel()
            pausar()
        elif opcion == "7":
            print("Gracias por usar el sistema del Hotel BuenDescanso. ¡Hasta pronto!")
            sys.exit()
        else:
            print("❌ Opción inválida.")
            pausar()

if __name__ == "__main__":
    menu_principal()

    mport os

ARCHIVO_USUARIOS = "data/usuarios.txt"

# Create the data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Write user credentials to the users.txt file
with open(ARCHIVO_USUARIOS, "w") as f:
    f.write("admin1,clave123\n")
    f.write("admin2,adminhotel\n")

print(f"Created {ARCHIVO_USUARIOS} with admin credentials.")

menu_principal()

menu_principal()

menu_principal()

    
       
    

           
        
        
          