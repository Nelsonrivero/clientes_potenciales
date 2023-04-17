import mysql.connector
import pandas as pd
from mysql.connector import Error

mydb  = mysql.connector.connect(host="localhost", 
                                    user="root", 
                                    password="", 
                                    db="nelson_clientes_potenciales")

mycursor = mydb.cursor()


print("█▀▀ █░░ █ █▀▀ █▄░█ ▀█▀ █▀▀ █▀   █▀█ █▀█ ▀█▀ █▀▀ █▄░█ █▀▀ █ ▄▀█ █░░ █▀▀ █▀")
print("█▄▄ █▄▄ █ ██▄ █░▀█ ░█░ ██▄ ▄█   █▀▀ █▄█ ░█░ ██▄ █░▀█ █▄▄ █ █▀█ █▄▄ ██▄ ▄█")

def menu_principal():
    print("--- Menú Principal ---")
    print("1. Ver registros")
    print("2. Insertar registro")
    print("3. Actualizar registro")
    print("4. Eliminar registro")
    print("5. Exportar datos a SQL")
    print("6. Importar datos desde SQL")
    print("7. Exportar datos a CSV")
    print("0. Salir")

    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        ver_registros()
    elif opcion == "2":
        insertar_registro()
    elif opcion == "3":
        actualizar_registro()
    elif opcion == "4":
        eliminar_registro()
    elif opcion == "5":
        exportar_sql()
    elif opcion == "6":
        importar_sql()
    elif opcion == "7":
        exportar_csv()
    elif opcion == "0":
        print("Saliendo....")
    else:
        print("Opción inválida")
        menu_principal()

def ver_registros():

    # Visualizar registros almacenados en la base de datos
    sql_read = "SELECT * FROM `clientes_potenciales`"
    mycursor.execute(sql_read)
    for base in mycursor:
        print(base)


    # Se regresa al menu para poder continuar con el programa, esto lo hacemos en las demas opciones.
    menu_principal()

def insertar_registro():

    # Insertar un nuevo registro, se piden los datos que se almacenaran en los campos de la DB
    nombre = str(input("Ingresa el nombre del nuevo registro: "))
    apellido = str(input("Ingresa el apellido del nuevo registro: "))
    edad = int(input("Ingresa la edad del nuevo registro: "))
    ingreso_mensual = float(input("Ingresa el ingreso mensual del nuevo registro: "))
    ingreso_anual = ingreso_mensual * 12 #para calcular el ingreso anual multiplicamos en mensual por doce meses que tiene el año
    puntaje_credito = int(input("Ingresa el puntaje de credito del nuevo registro: "))

    sql_insert = "INSERT INTO `clientes_potenciales` (`nombre`, `apellido`, `edad`, `ingreso_anual`, `puntaje_credito`) VALUES (%s,%s,%s,%s,%s)"
    # se contruye un variable contructora que lleva los datos a ingresar en la consulta
    valores = (nombre, apellido, edad, ingreso_anual, puntaje_credito)

    mycursor.execute(sql_insert, valores)
    
    mydb.commit()
    
    print(mycursor.rowcount, "registro insertado.")  

    menu_principal()

def actualizar_registro():

    # Actualizar los datos, se actualizan los datos que son mas propensos o tienen mayor probabilidad de ser actualizados

    # pedimos el id para que sea mas facil de identificar, porque por el nombre puede generar errores
    id = int(input("Ingresa el id en el que se encuentra guardado el registro: "))

    # Se establecen disferentes formas de actualizar los datos
    print("Que deseas actualizar: ")
    print("1.El ingreso Anual")
    print("2.El puntaje de credito")
    print("3.Ambos(Ingreso anual y el puntaje)") # Agregamos la opcion de actualizar los dos datos para ser mas optimos

    opcionUpdate = int(input("Ingresa el numero de la opcion: "))

    if opcionUpdate == 1:

        ingresoMensual = float(input("Ingresa el salario mensual: "))
        ingresoAnual = ingresoMensual * 12
        
        # utilizamos el %s para indicar posiciones en la variable constructura "values"
        sql_update = "UPDATE `clientes_potenciales` SET `ingreso_anual`=%s WHERE `id`=%s"

        # creamos la variable constructura con las varibles que utilizamos para almacenar los datos solicitados.
        values = (ingresoAnual, id) #ingresoAnual hace referancia al primer %s y id es el segundo %s


        mycursor.execute(sql_update , values)
        mydb.commit()
        print(mycursor.rowcount, "registro actualizado.")

    if opcionUpdate == 2:

        puntajeCredito = int(input("Ingresa el puntaje de credito: "))

        sql_update = "UPDATE `clientes_potenciales` SET `puntaje_credito`=%s WHERE `id`=%s"
        values = (puntajeCredito, id)


        mycursor.execute(sql_update , values)
        mydb.commit()
        print(mycursor.rowcount, "registro actualizado.")

    if opcionUpdate == 3:

        ingresoMensual = float(input("Ingresa el salario mensual: "))
        ingresoAnual = ingresoMensual * 12
        sql_update = "UPDATE `clientes_potenciales` SET `ingreso_anual`=%s WHERE `id`=%s"
        values = (ingresoAnual, id)

        mycursor.execute(sql_update , values)

        puntajeCredito = int(input("Ingresa el puntaje de credito: "))
        sql_update2 = "UPDATE `clientes_potenciales` SET `puntaje_credito`=%s WHERE `id`=%s"
        values2 = (puntajeCredito, id)

        mycursor.execute(sql_update2 , values2)

        mydb.commit()
        print(mycursor.rowcount, "registro actualizado.")    

    menu_principal()

def eliminar_registro():

    # Eliminamos los registros utilizando el "id" para evitar errores
    idDelete = int(input("Ingresa el id en el que se encuentra guardado el registro: "))

    sql_delete = "DELETE FROM `clientes_potenciales` WHERE (`id`='%s')"
    values=(idDelete,)

    mycursor.execute(sql_delete,values)

    mydb.commit()
    
    print(mycursor.rowcount, "registro(s) eliminados(s).")
    menu_principal()

def exportar_sql():

    #Exportamos los datos utilizando el metodo "w" que reemplaza el contenido anterior con el nuevo.
    try :
        mycursor.execute("SELECT * FROM `clientes_potenciales`")
        with open("clientes_potenciales.sql", "w") as f:
            for line in mycursor:
                f.write(str(line) + "\n")
        mycursor.close()
        mydb.close()
        print("Datos exportados a clientes_potenciales.sql")
    except Error as e:
        print(e)    

    menu_principal()

def importar_sql():
    # importamos los datos desde el archivos que creamos con la funcion exportar_sql
    df = pd.read_sql("SELECT * FROM `clientes_potenciales`", con=mydb)
    print(df.head())
    
    menu_principal()

def exportar_csv():
    # exportamos los datos en un formato CSV leidos con la funcion importar_sql
    df = pd.read_sql("SELECT * FROM `clientes_potenciales`", con=mydb)
    df.to_csv("clientes_potenciales.csv")

    menu_principal()


menu_principal()



