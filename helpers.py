
import os
from flask import redirect, request, session
from functools import wraps
from flask.helpers import flash
from conexion import get_sqlserver_connection1
import pandas as pd
from datetime import datetime
import locale



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin") == 1:
            return """<h3 class="p-5" style="
            color: red;
            margin: 2%;
            font-size: 6vh;
            width: fit-content;
            ">No tienes permiso para acceder a este recurso</h3>""", 403
        return f(*args, **kwargs)
    return decorated_function


def validarString(dato):
    if not dato or not dato.isalpha() or dato.isspace():
        return False

    return True


def validarDouble(dato):
    if not dato or not dato.replace(".", "").isdigit() or float(dato) < 1:
        return False

    return True

def exportar_historial(fecha_inicio, fecha_final):
    conn = get_sqlserver_connection1()
    query = """
        SELECT * FROM historial_llamadas
        where convert(date, fecha_registro) BETWEEN ? AND ? ORDER BY fecha_registro
    """
    df = pd.read_sql(query, conn, params=[fecha_inicio, fecha_final])
    conn.close()
    return df

def exportar_historial_telemarketing(fecha_inicio, fecha_final):
    conn = get_sqlserver_connection1()
    query = """
        SELECT * FROM telemarketing
        WHERE fecha BETWEEN ? AND ? ORDER BY fecha
    """
    df = pd.read_sql(query, conn, params=[fecha_inicio, fecha_final])
    conn.close()
    return df

def exportar_base_total(fecha_inicio, fecha_final):
    conn = get_sqlserver_connection1()
    query = """
        SELECT * FROM actual
        WHERE convert(date, fecha_suscripcion) BETWEEN ? AND ? ORDER BY fecha_suscripcion
    """
    df = pd.read_sql(query, conn, params=[fecha_inicio, fecha_final])
    conn.close()
    return df

def formatear_fecha(fecha):
    try:
        # Configurar el locale en español (puede variar según el sistema)
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        try:
            # Alternativa para algunos sistemas
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except:
            print("No se pudo configurar el locale en español, se usarán nombres en inglés.")
    
    # Formatear la fecha al formato deseado
    fecha_formateada = fecha.strftime("%d de %B %Y, %H:%M")
    
    return fecha_formateada
