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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

def initAnalyzer():

    analyzer = model.newAnalyzer()
    return analyzer

def loadInfo(analyzer):

    airportfile = cf.data_dir + "airports-utf8-small.csv"
    input_file = csv.DictReader(open(airportfile, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        model.addairport(analyzer, airport)

    routesfile = cf.data_dir + "routes-utf8-small.csv"
    routes_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    for routes in routes_file:
        model.addrutes(analyzer, routes) 

    worldcitiesfile = cf.data_dir + "worldcities-utf8.csv"
    city_file = csv.DictReader(open(worldcitiesfile, encoding="utf-8"),
                                delimiter=",")
    for city in city_file:
        model.addcities(analyzer, city)

    return analyzer

def totalAirperGraph(analyzer,tipo):

    return model.totalAirperGraph(analyzer,tipo)

def totalConnectionsperGraph(analyzer,tipo):

    return model.totalConnectionsperGraph(analyzer,tipo)
def carga_aeropuertos(analyzer):
    return model.carga_aeropuertos(analyzer)

def req1(analyzer):
    return model.req1(analyzer)

def req2(analyzer, iata1, iata2):
    return model.req2(analyzer, iata1, iata2)