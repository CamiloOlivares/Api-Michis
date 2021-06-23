from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_registros_peso():
    try:

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from registros_peso ''')

        result = cursor.fetchall()

        print(result)
        cursor.close()
        conn.close()

        for res in result:
            res['fecha'] = str(res['fecha']).split('+')[0]

        return jsonify({
            "ok": True,
            "message": "Get regitros peso funcionando",
            "registros_peso":
                result,
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e),  "message": "Get registros peso no funcionando"}), 400


get_registros_peso.methods = ['GET']


def get_registro_peso():
    try:
        id_registro_peso = request.args.get('id_registro_peso')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from registros_peso where id_registro_peso=%s''', id_registro_peso)

        result = cursor.fetchall()

        print(result)
        cursor.close()
        conn.close()

        for res in result:
            res['fecha'] = str(res['fecha']).split('+')[0]

        return jsonify({
            "id_registro": id_registro_peso,
            "ok": True,
            "message": "Get regitro peso funcionando",
            "registros_peso":
                result,
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e),  "message": "Get registro peso no funcionando"}), 400


get_registro_peso.methods = ['GET']


def post_registro_peso():
    try:
        id_animal = request.json.get('id_animal')
        peso = request.json.get('peso')
        observaciones = request.json.get('observaciones')
        fecha = request.json.get('fecha')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            '''  insert into registros_peso(id_animal,fecha,peso,observaciones) 
values(%s,%s,%s,%s)''', (id_animal, fecha, peso, observaciones))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Post registro peso funcionando"}), 200
    except Exception as e:
        print(e)
        return jsonify({"ok": False, "error": str(e), "message": "Post registro peso no funcionando"}), 400


post_registro_peso.methods = ['POST']


def get_pesos_intervalo():
    try:
        id_animal = request.json.get('id_animal')
        fecha_inicio = request.json.get('fecha_inicio')
        fecha_termino = request.json.get('fecha_termino')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            '''  SELECT id_animal,fecha,peso,observaciones
                FROM   registros_peso
                WHERE id_animal=%s AND fecha 
                BETWEEN %s
                AND %s;''', (id_animal, fecha_inicio, fecha_termino))
        result = cursor.fetchall()

        conn.commit()

        cursor.close()
        conn.close()
        for res in result:
            res['fecha'] = str(res['fecha']).split('+')[0]

        return jsonify({"ok": True, "result": result, "message": "get registro peso por fecha funcionando"}), 200
    except Exception as e:
        print(e)
        return jsonify({"ok": False, "error": str(e), "message": "Post registro peso por fecha no funcionando"}), 400


post_registro_peso.methods = ['POST']


def get_last_registro_peso():
    try:
        id_animal = request.args.get('id_animal')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from registros_peso where id_animal=%s order by fecha desc limit 1 ''', (id_animal,))

        result = cursor.fetchone()

        print(result)
        cursor.close()
        conn.close()

        result['fecha'] = str(result['fecha']).split('+')[0]

        return jsonify({
            "id_animal": id_animal,
            "ok": True,
            "message": "Get last regitro peso funcionando",
            "registro_peso":
                result,
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e),  "message": "Get last registro peso no funcionando"}), 400


get_last_registro_peso.methods = ['GET']
