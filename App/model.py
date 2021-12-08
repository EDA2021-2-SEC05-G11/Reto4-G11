"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config 
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newAnalyzer():

    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {}
    analyzer['IATAS'] =  mp.newMap(numelements=14000,
                                     maptype='PROBING')#,comparefunction=compareIATA)

    analyzer['aeropuertos'] = mp.newMap(numelements=181,
                                     maptype='PROBING',
                                     comparefunction=comparestr)

    analyzer['rutas'] = mp.newMap(numelements=39,
                                     maptype='PROBING',
                                     comparefunction=comparestr)

    analyzer['ciudades'] = lt.newList(datastructure='ARRAY_LIST')
                                     

    analyzer['digrafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=181,
                                              comparefunction=comparestr)

    analyzer['grafo'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=182,
                                              comparefunction=comparestr)
    analyzer['Aero_departure'] = lt.newList(datastructure='ARRAY_LIST')
    return analyzer

def addairport(analyzer, aeropuerto):
    iata = aeropuerto["IATA"]
    map_iata = analyzer['IATAS']
    mp.put(map_iata, iata, aeropuerto)
    lt.addLast(analyzer['Aero_departure'], iata)
    mp.put(analyzer["aeropuertos"], iata, aeropuerto)

    if not gr.containsVertex(analyzer['digrafo'], iata):
        gr.insertVertex(analyzer['digrafo'], iata)
    gr.insertVertex(analyzer['grafo'], iata)
    return analyzer

def addrutes(analyzer, rutas):

    origen = rutas["Departure"]
    destino = rutas["Destination"]
    distancia = float(rutas["distance_km"])

    edge = gr.getEdge(analyzer['digrafo'], origen, destino)   

    if edge == None:

        gr.addEdge(analyzer["digrafo"],origen,destino,distancia)  

    edge_1 = gr.getEdge(analyzer['grafo'], destino, origen)   

    if edge_1 != None:       
        #Comprobar si existe un arco de vuelta, osea saber si existe un camino  
        edge_2 = gr.getEdge(analyzer["grafo"],origen,destino )

        if edge_1 == None and edge_2 == None:
           gr.addEdge(analyzer['grafo'], origen, destino, distancia)

    return analyzer

def addcities(analyzer, ciudad):

    lt.addLast(analyzer["ciudades"], ciudad)

    return analyzer

def comparestr(stop, keyvaluestop):
  
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def totalAirperGraph(analyzer,tipo):
    """
    Retorna el total de aeropuertos (vertices) de los grafos
    """
    return gr.numVertices(analyzer[tipo])

def totalConnectionsperGraph(analyzer,tipo):
    """
    Retorna el total arcos de los grafos
    """
    
    return gr.numEdges(analyzer[tipo])

def carga_aeropuertos(analyzer):
    A = lt.firstElement(analyzer['Aero_departure'])
    B = lt.lastElement(analyzer['Aero_departure'])
    datos1 = mp.get(analyzer["IATAS"], A)["value"]
    datos2 = mp.get(analyzer["IATAS"], B)["value"]
    print(datos1)
    print(datos2) 

#Req 1
def comparar_interconecciones (a1,a2):
    return a1['Interconnections'] > a2['Interconnections']

def r1(analyzer):
    interconecciones = lt.newList(datastructure='ARRAY_LIST')
    vertices = gr.vertices(analyzer['digrafo'])
    for vertice in lt.iterator(vertices):
        entrada = gr.indegree(analyzer['digrafo'], vertice)
        salida = gr.outdegree(analyzer['digrafo'], vertice)
        conecciones_totales = entrada + salida
        if conecciones_totales == 0:
            continue
        aeropuerto=mp.get(analyzer['IATAS'], vertice)['value']
        info={'Airport':vertice,
              'Interconnections': conecciones_totales,
              'Name':aeropuerto['Name'],
              'City':aeropuerto['City'],
              'Country': aeropuerto['Country'],
              'Inbound': entrada,
              'Outbound': salida}
        lt.addLast(interconecciones,info)
    sa.sort(interconecciones, comparar_interconecciones)
    for i in interconecciones['elements']:
        print(i)
    