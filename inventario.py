import os
import sys
import sqlite3


def initialize_db():
    con = sqlite3.connect("mydb.db")
    cursor = con.cursor()
    
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS articulos (
           id INTEGER PRIMARY KEY,
           nombre TEXT,
           precio REAL,
           cantidad INTEGER,
           tipo TEXT,
           Fecha_ingreso Date,
           observaciones TEXT,
           deleted INTEGER DEFAULT 0
       )
    ''')
    
    con.commit()
    con.close()
    print("Base de datos inicializada correctamente.") # Esta es la confirmación


def agregarArticulo():
    os.system('cls')
    print('--AGREGAR ARTICULO--')
    print('')
    
    nombre = input("Ingrese el articulo: ")
    precio = input("Ingrese el precio del articulo: ")
    unidad = input("Ingrese la cantidad del articulo: ")
    tipo = input("Ingrese el tipo del articulo: ")
    fecha = input("Fecha de ingreso")
    observaciones = input("Ingrese las observaciones del articulo: ")
    
    con = sqlite3.connect("mydb.db") 
    cursor = con.cursor()
    cursor.execute("INSERT INTO articulos (nombre, precio,  unidades, tipo, fecha_ingreso, observaciones) values(?, ?, ?, ?, ?)", (nombre, precio,  unidad,  tipo, fecha, observaciones))
    con.commit()
    con.close()
    
    print("Articulo agregado")
    print("")
    print("[6] Volver al menu")
    print("[5] Salir")
    
    opcion = input("Elije una opcion: ")
    
    if opcion == "6":
        menu()
    elif opcion == "5":
        sys.exit()
def verArticulo():
    os.system('cls')
    print("--VER ARTICULO--")
    print("")
    
    con = sqlite3.connect("mydb.db")
    cursor = con.cursor()
    cursor.execute("select * from articulos") 
    
    print("--------------------------------------------------------------------------------------------------------------------")
    print("Nombre   \t\tPrecio  \t\tCantidad  \t\tTipo   \t\tFecah_ingreso    \t\tObservaciones")
    print("--------------------------------------------------------------------------------------------------------------------")
    
    for articulo in cursor:
        print(articulo[1],"\t\t",articulo[2],"\t\t"  ,articulo[3],"\t\t"     ,articulo[4],"\t\t",articulo[5])
        print("")
        
    con.close()
    
    
    print("Revision de los articulos")
    print("Articulos Verificados")
    print("")
    print("[6] Volver al menu")
    print("[5] Salir")
    
    opcion = input("Elije una opcion: ")
    
    if opcion == "6":
        menu()
    elif opcion == "5":
        sys.exit()
        
def modificarArticulo():
    os.system('cls')
    print("--Modificar Producto--")
    print("")
    
    con = sqlite3.connect("mydb.db")
    cursor = con.cursor()
    cursor.execute("select nombre from articulos")
    
    print("Articulos disponibles:")
    for articulo in cursor:
        print(articulo[0])
    print("")
    
    codigo = input("Ingresa el nombre del articulo a modificar: ")
    
    nombre = input("Ingrese el nuevo nombre del articulo: ")
    precio = input("Ingrese el nuevo precio del articulo: ")
    unidad = input("Ingrese la nueva cantidad del articulo: ")
    tipo = input("Ingrese el nuevo tipo del articulo: ")
    observaciones = input("Ingrese las nuevas observaciones del articulo: ")
    
    sql = "update articulos set nombre=?, precio=?, unidades=?, tipo=?, observaciones=? where nombre=?"
    cursor.execute(sql, (nombre, precio,  unidad, tipo, observaciones))
    
    con.commit()
    con.close()
    
    print("Articulo modificado")
    print("")
    print("[6] Volver al menu")
    print("[5] Salir")
    
    opcion = input("Elije una opcion: ")
    
    if opcion == "6":
        menu()
    elif opcion == "5":
        sys.exit()

def eliminarArticulo():
    os.system('cls')
    con = sqlite3.connect("mydb.db")
    cursor = con.cursor()
    cursor.execute("select nombre from articulos")
    
    print("--Eliminar Producto--")
    print("")
    
    for articulo in cursor:
        print(articulo[0])
    
    print("")
    codigo = input("Ingresa el nombre del articulo a Eliminar: ")
    
    sql = "delete from articulos where nombre=?"
    cursor.execute(sql, (codigo,))
    con.commit()
    con.close()
    
    print("Articulo Eliminado")
    print("")
    print("[6] Volver al menu")
    print("[5] Salir")
    
    opcion = input("Elije una opcion: ")
    
    if opcion == "6":
        menu()
    elif opcion == "5":
        sys.exit()
     
     
def menu():
    os.system('cls')
    print("MENU PRINCIPAL")
    print("[1] Agregar artículo")
    print("[2] Ver artículos")
    print("[3] Modificar artículo")
    print("[4] Eliminar artículo")
    print("[5] Salir")
    
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        agregarArticulo()
    elif opcion == "2":
        verArticulo()
    elif opcion == "3":
        modificarArticulo()
    elif opcion == "4":
        eliminarArticulo()
    elif opcion == "5":
        sys.exit()
    else:
        print("Opción inválida. Inténtalo de nuevo.")
        menu()

if __name__ == "__main__":
    initialize_db()
    menu()

    
    
    
    
    