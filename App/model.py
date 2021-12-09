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
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs.dijsktra import Dijkstra, pathTo, distTo
from DISClib.Algorithms.Graphs import prim
from DISClib.Utils import error as error
#import haversine
#from haversine import haversine, inverse_haversine, Direction
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

def newAnalyzer():

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
    analyzer['Ciudad'] =mp.newMap(10500,
                                  maptype='CHAINING',
                                  loadfactor=4)
    analyzer['latitude'] = om.newMap(omaptype="RBT")
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

    lat = round(float(aeropuerto["Latitude"]), 3)
    
    keyval = om.get(analyzer["latitude"], lat)

    if keyval is None:
        airports = lt.newList()
        om.put(analyzer["latitude"], lat, airports)
    else:
        airports = me.getValue(keyval)
    return analyzer

def addrutes(analyzer, rutas):

    origen = rutas["Departure"]
    destino = rutas["Destination"]
    distancia = float(rutas["distance_km"])

    edge = gr.getEdge(analyzer['digrafo'], origen, destino)   

    if edge == None:

        gr.addEdge(analyzer["digrafo"],origen,destino,distancia)  

    edge_ = gr.getEdge(analyzer['digrafo'], destino, origen)   

    if edge_ != None:       
        #Comprobar si existe un arco de vuelta, osea saber si existe un camino  
        edge_1 = gr.getEdge(analyzer['grafo'], destino, origen)   
        edge_2 = gr.getEdge(analyzer["grafo"],origen,destino )

        if edge_1 == None and edge_2 == None:
           gr.addEdge(analyzer['grafo'], origen, destino, distancia)

    return analyzer

def addcities(analyzer, ciudad):
    ciudades=analyzer['Ciudad']
    nombres_ciu=ciudad['city_ascii']
    existe = mp.contains(ciudades,nombres_ciu)
    lt.addLast(analyzer["ciudades"], ciudad)
    if existe:
        ciudad=me.getValue(mp.get(ciudades,nombres_ciu))
    else:
        
        mp.put(ciudades,nombres_ciu,ciudad)
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

def total_ciudades(analyzer):
    return (lt.size(analyzer["ciudades"]))

def carga_ciudades(analyzer,cantidad):
    print(lt.getElement(analyzer["ciudades"],1))
    print(lt.getElement(analyzer["ciudades"],cantidad))

#Req 1
def comparar_interconecciones (a1,a2):
    return a1['Interconnections'] > a2['Interconnections']

def req1(analyzer):
    print(analyzer["rutas"])
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
#Req 2
def req2(analyzer, iata1, iata2):

    dic_iata1=mp.get(analyzer["aeropuertos"], iata1)["value"]
    dic_iata2=mp.get(analyzer["aeropuertos"], iata2)["value"]
    print("Aeropuerto con codigo iata " + iata1)
    print(quitar_exedentes(dic_iata1))
    print("\n")
    print("Aeropuerto con codigo iata " + iata2)
    print(quitar_exedentes(dic_iata2))

    componentes = scc.connectedComponents(scc.KosarajuSCC(analyzer['digrafo']))
    comp_fuerte = scc.stronglyConnected(scc.KosarajuSCC(analyzer['digrafo']),iata1, iata2)
    print("\nHay " + str(componentes) + " clústeres presentes en la red de transporte aéreo." )

    if comp_fuerte == False:

        respuesta = ("\nLos aeropuertos identificados con el iata " + iata1 + " y " + iata2 + " no estan en el mismo clúster\n")

    elif comp_fuerte == True:

        respuesta = ("\nLos aeropuertos identificados con el iata " + iata1 + " y " + iata2 + " estan en el mismo clúster\n")

    return respuesta 

def quitar_exedentes(dic):

    respuesta={}
    respuesta["IATA"]=dic["IATA"]
    respuesta["Name"]=dic["Name"]
    respuesta["City"]=dic["City"]
    respuesta["Country"]=dic["Country"]

    return respuesta 
#Req 3
def Req3_(analyzer,city):
    
    Coordenadas_= (float(city['lat']), float(city['lng']))
    
    Latitud= analyzer['latitude']
    Distancia_Km=10
    
    Lista_ = lt.newList(datastructure='ARRAY_LIST')

    while lt.size(Lista_) == 0:
        Norte = haversine.inverse_haversine(Coordenadas_,  Distancia_Km,Direction.NORTH)
        Sur = haversine.inverse_haversine(Coordenadas_,  Distancia_Km,Direction.SOUTH)
        Oeste = haversine.inverse_haversine(Coordenadas_,  Distancia_Km,Direction.WEST)
        Este = haversine.inverse_haversine(Coordenadas_,  Distancia_Km,Direction.EAST)
        
        latitud_aero = om.values(Latitud, Sur[0], Norte[0])
        for list in lt.iterator(latitud_aero):
            for airport in lt.iterator(list):
                if float(airport['Longitude']) > Oeste[1] and float(airport['Longitude']) < Este[1]:
                    lt.addLast(Lista_,airport)
        Distancia_Km+=10

    if lt.size(Lista_)!=1:
        for i in lt.iterator(Lista_):
            Coordenadas_aero = (float(i['Latitude']), float(i['Longitude']))
            distancia = haversine.haversine(Coordenadas_,Coordenadas_aero)
            if distancia < Distancia_Km:
                aero = i
                Distancia_Km = distancia
    else:
        aero = lt.firstElement(Lista_)
    return aero, Distancia_Km

def req3(catalog, city1, city2):
    aero__1, distancia__1 = Req3_(catalog, city1)
    aero__2, distancia__2 = Req3_(catalog, city2)
    dijsktra = Dijkstra(catalog['dir_connections'], aero__1["IATA"])
    return pathTo(dijsktra, aero__1["IATA"]), distancia__1, distTo(dijsktra, aero__2['IATA']), distancia__2
#Req4

def req4(analyzer, origen, millas):
    
    mst = prim.PrimMST(analyzer['grafo'])
    km = millas * 1.60
    nuevo_grafo = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=1000,
                                              comparefunction=comparestr)
    primmst=(prim.prim(analyzer["grafo"], mst,origen))


    for i in lt.iterator(primmst['edgeTo']['table']):
    
        if i['key'] != None:
            
            origen = i['value']['vertexA']
            destino = i['value']['vertexB']
            distancia = i['value']['weight']

            if not gr.containsVertex(nuevo_grafo, origen):
                gr.insertVertex(nuevo_grafo, origen)
            if not gr.containsVertex(nuevo_grafo, destino):
                gr.insertVertex(nuevo_grafo, destino)
            if gr.getEdge(nuevo_grafo, origen, destino) == None:
                gr.addEdge(nuevo_grafo, origen, destino, distancia)

    print("Hay " + str(gr.numVertices(nuevo_grafo)) + " posibles aeropuertos")
    print("La distancia entre los aeropuertos es de " + str(round(prim.weightMST(analyzer["grafo"],mst),2)) + " Km")
    print("La cantidad de millas de viaje disponibles del usuario es de " + str(round(km,2)) + " km\n")

    suma = 0
    edge = None
    dic_final = {}
    lista_final = []
    df = dfs.DepthFirstSearch(analyzer["grafo"], origen)
    for i in lt.iterator(df['visited']['table']):
        if i['key'] != None:
          dic_final = {} 
          if  i["value"]["edgeTo"] != None:
             edge=gr.getEdge(analyzer["grafo"], i["key"], i["value"]["edgeTo"])
             dic_final["Departure"]= edge["vertexA"]
             dic_final["Destination"] = edge["vertexB"]
             dic_final["distance km"] = edge["weight"]
             suma += edge["weight"]
             lista_final.append(dic_final)
    print("El camino mas largo posible es de " + str(round(suma,2)) + " km")    
    print("Los detalles del camino mas largo son: \n")   
    print(lista_final)
    milla_suma= round(suma,2)/1.60
    necesidad = round((millas - (round(milla_suma,2)*2)),2)

    if necesidad > 0:
        result = "\nAl usuario le sobran " + str(necesidad) + " millas"
    else:
        result = "\nAl usuario le faltan " + str(abs(necesidad)) + " millas"
    return result 


#Req5

def req5(analyzer, iata):

    aeropuertos_afectados = lt.newList('ARRAY_LIST')
    conecciones = gr.adjacents(analyzer['grafo'], iata)

    for i in range(1, lt.size(conecciones)+1):
        aeropuerto = lt.getElement(conecciones,i)
        dic_aeropuerto = mp.get(analyzer['aeropuertos'], aeropuerto)["value"]
        info_aeropuerto = quitar_exedentes(dic_aeropuerto)
        lt.addLast(aeropuertos_afectados, info_aeropuerto)

    print("Hay " + str(lt.size(aeropuertos_afectados))+ " aeropuertos afectados tras el cierre del aeropuerto " + iata)
    
    if lt.size(aeropuertos_afectados) > 6:
     resultado=lt.subList(aeropuertos_afectados, 1, 3)
     final=lt.subList(aeropuertos_afectados, - 3, 3)

     for i in range(lt.size(final)+1):
        lt.addLast(resultado, lt.getElement(final, i))
    else:
     resultado= aeropuertos_afectados
    return resultado
  

