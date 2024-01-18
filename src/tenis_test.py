from tenis import *


def test_lee_partidos_tenis(partidos):
    print("EJERCICIO  1==================================================")
    print("Test de 'lee_partidos_tenis'")
    print(f"Registros leídos: {len(partidos)}")
    print(f"Dos primeros partidos:\n{partidos[:2]}")


def test_partidos_menos_errores(partido):
    print("EJERCICIO  2==================================================")
    print("\nTest de 'partidos_menos_errores'")
    print(f"El partido con menos errores es  {partido}")


def test_jugador_mas_partidos(jugador):
    print("EJERCICIO  3==================================================")
    print("\nTest de 'jugador_mas_partidos'")
    print(f"El jugador que ha jugado más partidos es {jugador[0]}, con un total de {jugador[1]} partidos")


def test_tenista_mas_victorias(tenista, f1=None, f2=None):
    print("EJERCICIO  4==================================================")
    print(f"Test de 'tenista_mas_victorias' fecha1={f1}, fecha2={f2}")
    print(f"El tenista con más victorias entre las fechas {f1} y {f2} es {tenista}")


def test_media_errores_por_jugador(partidos):
    media_errores = media_errores_por_jugador(partidos)
    print("EJERCICIO  5==================================================")
    print("Test de 'media_errores_por_jugador'")
    print(f"La media de errores por jugador, de menos a más errores es")
    for i in range(0, len(media_errores)):
        print(f"{i+1}-{media_errores[i]}")


def test_jugadores_mayor_porcentaje_victorias(partidos):
    print("EJERCICIO  6==================================================")
    porcentaje_jugadores = jugadores_mayor_porcentaje_victorias(partidos)
    print("Test de 'jugadores_mayor_porcentaje_victorias'")
    print("El porcentaje de victorias de cada jugador (ordendo de mayor a menor) es")
    for i in range(0, len(porcentaje_jugadores)):
        print(f"{i+1}-{porcentaje_jugadores[i]}")

def test_n_tenistas_con_mas_errores(partidos, n):
    print("EJERCICIO  7==================================================")
    errores = n_tenistas_con_mas_errores(partidos, n)
    print(f"Test de 'n_tenistas_con_mas_errores' n={n}")
    print(f"Los {n} tenistas con mas errores son:")
    for i in range(0, len(errores)):
        print(f"{i+1}-{errores[i]}")

def test_fechas_por_jugador(partidos):
    print("EJERCICIO  8==================================================")
    fechas = fechas_por_jugador(partidos)
    print("Test de 'fechas_por_jugador'")
    print("Las fechas de cada partido por jugador son")
    for i in fechas:
        print(f"{i[0]} --> {fechas[1]}")
    

if __name__ == "__main__":
    partidos = lee_partidos_tenis("data/tenis.csv")
    # test_lee_partidos_tenis(partidos)
    # test_partidos_menos_errores(partidos_menos_errores(partidos))
    # test_jugador_mas_partidos(jugador_mas_partidos(partidos))
    # test_tenista_mas_victorias(tenista_mas_victorias(partidos))
    # test_media_errores_por_jugador(partidos)
    # test_jugadores_mayor_porcentaje_victorias(partidos)
    # test_n_tenistas_con_mas_errores(partidos, 5)
    test_fechas_por_jugador(partidos)