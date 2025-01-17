﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\nBienvenido")
    print("A- Cargar información en el catálogo")
    print("1- Encontrar puntos de interconexión aérea.")
    print("2- Encontrar clústeres de tráfico aéreo.")
    print("3- Encontrar la ruta más corta entre ciudades.")
    print("4- Utilizar las millas de viajero.")
    print("5- Cuantificar el efecto de un aeropuerto cerrado.")
    print("6- Comparar con servicio WEB externo.")

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if str(inputs[0]).lower() == "a":
        print("Cargando información de los archivos ....")
        cont = controller.initAnalyzer()
        cont = controller.loadInfo(cont)
        print("==== Rutas del aeropuerto Digrafo ====")
        print("Vertices: "+str(controller.totalAirperGraph(cont,"digrafo"))+" aeropuertos cargados. ")
        print("Arcos "+ str(controller.totalConnectionsperGraph(cont,"digrafo"))+" rutas cargadas. ")
        print("El primero y ultimo aeropuerto cargado en el Digrafo son: ")
        controller.carga_aeropuertos(cont)
        print("\n==== Rutas del aeropuerto grafo ====")
        print("Vertices: " +str(controller.totalAirperGraph(cont,"grafo"))+" aeropuertos cargados. ")
        print("Arcos: "+str(controller.totalConnectionsperGraph(cont,"grafo"))+" rutas cargadas. ")
        print("El primero y ultimo aeropuerto cargado en el grafo son: ")
        controller.carga_aeropuertos(cont)
        print("\n==== Ciudades ====")
        cantidad=controller.total_ciudades(cont)
        print("El numero de ciudades es de " + str(cantidad))
        print("La primera y ultima ciudad carga son: ")
        controller.carga_ciudades(cont,cantidad)
        
    elif int(inputs[0]) == 1:
        controller.req1(cont)

    elif int(inputs[0]) == 2:
        iata1 = str(input("Ingrese el identificador (IATA) del primer aeropuerto: ")).upper()
        iata2 = str(input("Ingrese el identificador (IATA) del segundo aeropuerto: ")).upper()
        print("\n")
        print(controller.req2(cont, iata1, iata2))
    elif int(inputs[0]) == 3:

        Ciudad_salida=input('Ciudad de salida: ')
        Ciudad_destino=input('Ciudad de llegada: ')
        salida_=mp.get(cont['Ciudad'],Ciudad_salida)['value']
        destino_=mp.get(cont['Ciudad'],Ciudad_destino)['value']
        controller.req3(cont,salida_,destino_)
            
        
    elif int(inputs[0]) == 4:
        ciudad = str(input("Ingrese el identificador (IATA) del aeropuerto: ")).upper()
        millas = float(input("Ingrese la cantidad de millas disponibles: "))
        print(controller.req4(cont, ciudad, millas))
    elif int(inputs[0]) == 5:
        iata= str(input("Ingrese el identificador (IATA) del aeropuerto: ")).upper()
        print(controller.req5(cont, iata))
    else:
        sys.exit(0)
sys.exit(0)
