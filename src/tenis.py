from collections import defaultdict
from typing import Dict, NamedTuple, List, Tuple
from parsers import *
import csv


Parcial = NamedTuple('Parcial', [('juegos_j1',int), ('juegos_j2',int)])
PartidoTenis = NamedTuple('PartidoTenis', [('fecha',datetime.date), ('jugador1',str), ('jugador2',str), ('superficie',str), ('resultado', List[Parcial]), ('errores_nf1',int), ('errores_nf2',int)])


def lee_partidos_tenis(ruta_fichero: str) -> List[PartidoTenis]:
    res = []

    with open(ruta_fichero, encoding="UTF-8") as f:
        lector = csv.reader(f, delimiter=";")

        for fecha, jugador1, jugador2, superficie, set1, set2, set3, errores_nf1, errores_nf2 in lector:
            fecha = parseo_fecha(fecha)
            jugador1 = jugador1.strip()
            jugador2 = jugador2.strip()
            superficie = superficie.strip()
            resultado = parsea_set(set1, set2, set3)
            errores_nf1 = int(errores_nf1)
            errores_nf2 = int(errores_nf2)

            res.append(PartidoTenis(fecha, jugador1, jugador2, superficie, resultado, errores_nf1, errores_nf2))
    return res

def parsea_set(set1: str, set2: str, set3: str) -> Parcial:
    lista_parciales = []
    puntos_j1 = 0
    puntos_j2 = 0
    cadena_puntos = set1+";"+set2+";"+set3
    lista_sets = cadena_puntos.split(";")

    for set in lista_sets:
        puntos_set = set.split("-")
        puntos_j1 = int(puntos_set[0])
        puntos_j2 = int(puntos_set[1])
        lista_parciales.append(Parcial(puntos_j1, puntos_j2))

    return lista_parciales


def partidos_menos_errores(partidos: List[PartidoTenis]) -> PartidoTenis:
    '''
    Recibe una lista de tipo PartidoTenis y devuelve el partido con menor número de errores no forzados
    entre los dos jugadores.
    '''
    partido_errores = min(partidos, key = lambda partido:partido.errores_nf1+partido.errores_nf2)
    return partido_errores


def jugador_mas_partidos(partidos: List[PartidoTenis]) -> Tuple[str, int]:
    '''
    Recibe una lista de tipo PartidoTenis y devuelve una tupla con el nombre del jugador que más partidos
    ha jugado y el número de partidos.
    '''
    jugadores_partidos = defaultdict(int)

    for partido in partidos:
        jugadores_partidos[partido.jugador1] += 1
        jugadores_partidos[partido.jugador2] += 1

    return max(jugadores_partidos.items(), key=lambda x:x[1])


def tenista_mas_victorias(partidos: List[PartidoTenis], f1:datetime=None, f2:datetime=None) -> Tuple[str, int]:
    '''
    Recibe una lista de tuplas de tipo PartidoTenis, y dos fechas, ambas de tipo date, y con valor por
    defecto None. Devuelve el nombre del tenista que ha tenido más victorias en los partidos jugados
    entre las fechas (ambas inclusive). Si la primera fecha es None, la función devuelve el tenista con
    más victorias hasta esa fecha (inclusive). Si la segunda fecha es None, la función devuelve el
    tenista con más victorias desde esa fecha (inclusive). Finalmente, si las dos fechas son None, la
    función devuelve el tenista con más victorias de toda la lista, independientemente de la fecha.
    Para implementar esta función defina la siguiente función auxiliar: a. ganador:** recibe una tupla
    de tipo PartidoTenis y devuelve el nombre del jugador que ganó ese partido.
    '''
    dict_victorias_tenista = defaultdict(int)

    for partido in partidos:
        if (f1 is None or partido.fecha >= f1) and (f2 is None or partido.fecha<=f2):
            dict_victorias_tenista[ganador(partido)] += 1

    return max(dict_victorias_tenista.items(), key=lambda x:x[1])

def ganador(lista_partidos):
    resultado = lista_partidos.resultado
    if resultado[0].juegos_j1 > resultado[0].juegos_j2 and resultado[1].juegos_j1 > resultado[1].juegos_j2:
        res = lista_partidos.jugador1
    elif resultado[0].juegos_j1 < resultado[0].juegos_j2 and resultado[1].juegos_j1 < resultado[1].juegos_j2:
        res = lista_partidos.jugador2
    elif resultado[2].juegos_j1 > resultado[2].juegos_j2:
        res = lista_partidos.jugador1
    elif resultado[2].juegos_j1 < resultado[2].juegos_j2:
        res = lista_partidos.jugador2
    return res
    

def media_errores_por_jugador(partidos: List[PartidoTenis]) -> List[Tuple[(str, float)]]:
    '''
    Recibe una lista de tuplas de tipo PartidoTenis y devuelve una lista de tuplas ordenadas con el
    nombre de cada jugador y su media de errores no forzados. La lista estará ordenada por la media
    de errores de menor a mayor.
    '''
    dict_errores_jugador = defaultdict(list)
    dict_media_errores = defaultdict(int)

    for partido in partidos:
        dict_errores_jugador[partido.jugador1].append(partido.errores_nf1)
        dict_errores_jugador[partido.jugador2].append(partido.errores_nf2)

    for jugador, lista_errores in dict_errores_jugador.items():
        dict_media_errores[jugador] = sum(lista_errores)/len(lista_errores)

    return sorted(dict_media_errores.items(), key=lambda x:x[1])


def jugadores_mayor_porcentaje_victorias(partidos: List[PartidoTenis]) -> List[Tuple[str, float]]:
    '''
    Recibe una lista de tuplas de tipo PartidoTenis y devuelve una lista de tuplas con el nombre de
    cada jugador y el porcentaje de victorias. La lista estará ordenada por el porcentaje de
    victorias de mayor a menor.
    '''
    dict_victorias_tenista = defaultdict(lambda:[0, 0])
    dict_porcentaje_victorias = defaultdict(float)

    for partido in partidos:
        if partido.jugador1 == ganador(partido):
            dict_victorias_tenista[partido.jugador1][0] += 1
        else:
            dict_victorias_tenista[partido.jugador2][0] += 1
        dict_victorias_tenista[partido.jugador1][1] += 1
        dict_victorias_tenista[partido.jugador2][1] += 1

    for tenista, partidos in dict_victorias_tenista.items():
        dict_porcentaje_victorias[tenista] += (partidos[0]/partidos[1])

    return sorted(dict_porcentaje_victorias.items(), key=lambda x:x[1], reverse=True)


def n_tenistas_con_mas_errores(partidos: List[PartidoTenis], n:int=None) -> List[str]:
    '''
    Recibe una lista de tuplas de tipo PartidoTenis y un número n, con valor por defecto None, y
    devuelve una lista con los nombres de los n tenistas que han acumulado más errores no forzados
    en el total de partidos que han jugado. Si n es None, entonces devuelve todos los tenistas de
    la lista de tuplas ordenados de mayor a menor número de errores no forzados. (2 puntos)
    '''
    dict_errores_tenistas = defaultdict(int)
    
    for partido in partidos:
        dict_errores_tenistas[partido.jugador1] += partido.errores_nf1
        dict_errores_tenistas[partido.jugador2] += partido.errores_nf2

    return sorted(dict_errores_tenistas.items(), key=lambda x:x[1], reverse=True)[:n]


def fechas_ordenadas_por_jugador(partidos: List[PartidoTenis]) -> Dict[str, List[datetime]]:
    '''
    Recibe una lista de tuplas de tipo PartidoTenis y devuelve un diccionario en el que a cada jugador
    le hace corresponder una lista ordenada con las fechas de sus partidos.
    '''
    fechas_jugador = defaultdict(list)
    fechas_jugador_ordenado = defaultdict(list)

    for partido in partidos:
        fechas_jugador[partido.jugador1].append(partido.fecha)
        fechas_jugador[partido.jugador2].append(partido.fecha)

    for jugador, lista_fechas in fechas_jugador.items():
        fechas_jugador_ordenado[jugador] = sorted(lista_fechas)

    return fechas_jugador_ordenado


def num_partidos_nombre(partidos: List[PartidoTenis], nom_tenista: str) -> Dict[str, List[Tuple[int, int]]]:
    '''
    Recibe el nombre de un tenista y devuelve un diccionario en el que las claves son las superficies y los
    valores una tupla con el número de partidos jugados y ganados por el tenista en la superficie dada como clave.
    '''
    dict_partidos_superficies = defaultdict(lambda: (0, 0))

    for partido in partidos:
        if partido.jugador1 == nom_tenista or partido.jugador2 == nom_tenista:
            partidos_jugados, partidos_ganados = dict_partidos_superficies[partido.superficie]
            partidos_jugados += 1
            if ganador(partido) == nom_tenista:
                partidos_ganados += 1
            dict_partidos_superficies[partido.superficie] = (partidos_jugados, partidos_ganados)

    return dict_partidos_superficies