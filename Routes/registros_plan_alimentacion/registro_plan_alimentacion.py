from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_registro_plan():
    try:
        id_plan_alimentacion = request.args.get('id_plan_alimentacion')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from registros_plan_alimentacion where id_plan_alimentacion=%s''', id_plan_alimentacion)

        result = cursor.fetchall()

        print(result)
        cursor.close()
        conn.close()

        for res in result:
            res['fecha'] = str(res['fecha']).split('+')[0]

        return jsonify({
            "id_plan_alimentacion": id_plan_alimentacion,
            "ok": True,
            "message": "Get registro plan alimentacion funcionando",
            "medicamento":
                result,
        }), 200
    except:
        return jsonify({"ok": False, "message": "Get registro plan alimentacion no funcionando"}), 400


get_registro_plan.methods = ['GET']


def post_registro_plan():
    try:
        id_plan_alimentacion = request.json.get('id_plan_alimentacion')
        fecha = request.json.get('fecha')
        id_cuidador = request.json.get('id_cuidador')
        observaciones = request.json.get('observaciones')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            '''  insert into registros_plan_alimentacion(id_plan_alimentacion,fecha,id_cuidador,observaciones,cumplido)
    values(%s,%s,%s,%s,true) ''', (id_plan_alimentacion, fecha, id_cuidador, observaciones))

        #result = cursor.fetchone()
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Post registro plan funcionando"}), 200
    except:
        return jsonify({"ok": False, "message": "Post registro plan no funcionando"}), 400


post_registro_plan.methods = ['POST']
