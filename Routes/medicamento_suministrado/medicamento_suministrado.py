from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_medicamento_suministrado():
    try:
        id_medicamento = request.args.get('id_medicamento')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from medicamentos_suministrados where id_medicamento=%s''', id_medicamento)

        result = cursor.fetchall()

        print(result)
        cursor.close()
        conn.close()

        for res in result:
            res['fecha'] = str(res['fecha']).split('+')[0]

        return jsonify({
            "id_medicamento": id_medicamento,
            "ok": True,
            "message": "Get medicamento suministrado funcionando",
            "medicamento":
                result,
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get medicamento suministrado no funcionando"}), 400


get_medicamento_suministrado.methods = ['GET']


def post_medicamento_suministrado():
    try:
        id_cuidador = request.json.get('id_cuidador')
        id_medicamento = request.json.get('id_medicamento')
        observaciones = request.json.get('observaciones')
        fecha = request.json.get('fecha')
        cumplido = request.json.get('cumplido')
        nombre_cuidador = request.json.get('nombre_cuidador')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            '''  insert into medicamentos_suministrados(id_cuidador,id_medicamento,observaciones,fecha,cumplido,nombre_cuidador) 
values(%s,%s,%s,%s,%s,%s)  ON CONFLICT(id_medicamento,fecha) DO UPDATE SET 
    (id_cuidador,observaciones,cumplido,nombre_cuidador) = (EXCLUDED.id_cuidador, EXCLUDED.observaciones, EXCLUDED.cumplido, EXCLUDED.nombre_cuidador);''', (id_cuidador, id_medicamento, observaciones, fecha, cumplido,nombre_cuidador))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Post medicamento suministrado funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Post medicamento suministrado no funcionando"}), 400


post_medicamento_suministrado.methods = ['POST']
