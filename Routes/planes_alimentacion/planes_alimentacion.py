from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_planes_alimentacion():
    try:
        id_plan_alimentacion = request.args.get('id_plan_alimentacion')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from planes_alimentacion where id_plan_alimentacion=%s''', id_plan_alimentacion)

        result = cursor.fetchone()

        print(result)
        cursor.close()
        conn.close()

        return jsonify({
            "id_plan_alimentacion": id_plan_alimentacion,
            "ok": True,
            "message": "Get plan alimentacion funcionando",
            "medicamento":
                result,
        }), 200
    except:
        return jsonify({"ok": False, "message": "Get plan alimentacion no funcionando"}), 400


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

        return jsonify({"ok": True, "result": result, "message": "Post medicamento funcionando"}), 200
    except:
        return jsonify({"ok": False, "message": "Post medicamento no funcionando"}), 400


post_planes_alimentacion.methods = ['POST']
