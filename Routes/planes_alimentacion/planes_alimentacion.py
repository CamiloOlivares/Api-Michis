from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_planes_alimentacion():
    try:
        id_animal = request.args.get('id_animal')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from planes_alimentacion where id_animal=%s''', (id_animal,))

        result = cursor.fetchall()

        cursor.close()
        conn.close()
        for res in result:
            res['fecha_inicio'] = str(res['fecha_inicio']).split('+')[0]

        return jsonify({
            "id_animal": id_animal,
            "ok": True,
            "message": "Get plan alimentacion funcionando",
            "planes":
                result,
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get plan alimentacion no funcionando"}), 400


get_planes_alimentacion.methods = ['GET']


def post_planes_alimentacion():
    try:
        id_animal = request.json.get('id_animal')
        fecha_inicio = request.json.get('fecha_inicio')
        observaciones = request.json.get('observaciones')
        #foto = request.json.get('foto')
        nombre_alimento = request.json.get('nombre_alimento')
        marca = request.json.get('marca')
        dosis = request.json.get('dosis')
        periodicidad = request.json.get('periodicidad')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            '''  insert into planes_alimentacion(id_animal,fecha_inicio,observaciones,nombre_alimento,marca,dosis,periodicidad)
    values(%s,%s,%s,%s,%s,%s,%s) returning id_plan_alimentacion''', (id_animal, fecha_inicio, observaciones, nombre_alimento, marca, dosis, periodicidad))

        result = cursor.fetchone()
        conn.commit()
        print(result)
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "result": result, "message": "Post plan alimentacion funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Post plan alimentacion no funcionando"}), 400


post_planes_alimentacion.methods = ['POST']


def get_all_planes_alimentacion():
    try:

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from planes_alimentacion''')

        result = cursor.fetchall()

        print(result)
        cursor.close()
        conn.close()

        #result['fecha_inicio'] = str(result['fecha_inicio']).split('+')[0]

        return jsonify({
            "ok": True,
            "message": "Get plan alimentacion funcionando",
            "result":
                result,
        }), 200
    except:
        return jsonify({"ok": False, "message": "Get plan alimentacion no funcionando"}), 400


get_all_planes_alimentacion.methods = ['GET']


def delete_plan_alimentacion():
    try:
        id_plan_alimentacion = request.args.get('id_plan_alimentacion')
        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' delete from planes_alimentacion where id_plan_alimentacion=%s''', (id_plan_alimentacion,))
        conn.commit()

        # print(result[0]['fecha_nacimiento'])
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Delete planes_alimentacion funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Delete planes_alimentacion no funcionando"}), 400


delete_plan_alimentacion.methods = ['DELETE']
