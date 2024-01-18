from datetime import datetime


def parseo_fecha(cadena):
    return datetime.strptime(cadena, "%d/%m/%Y").date()
