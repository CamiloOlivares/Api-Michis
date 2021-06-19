from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_medicamento():
    try:
        id_medicamento = request.args.get('id_medicamento')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from medicamentos where id_medicamento=%s''', id_medicamento)

        result = cursor.fetchone()

        print(result)
        cursor.close()
        conn.close()

        result['fecha_inicio'] = str(result['fecha_inicio']).split('+')[0]
        result['fecha_termino'] = str(result['fecha_termino']).split('+')[0]

        return jsonify({
            "id_medicamento": id_medicamento,
            "ok": True,
            "message": "Get medicamento funcionando",
            "medicamento":
                result,
        }), 200
    except:
        return jsonify({"ok": False, "message": "Get medicamento no funcionando"}), 400


get_medicamento.methods = ['GET']


def post_medicamento():
    try:
        id_animal = request.json.get('id_animal')
        fecha_inicio = request.json.get('fecha_inicio')
        fecha_termino = request.json.get('fecha_termino')
        #foto = request.json.get('foto')
        nombre_medicamento = request.json.get('nombre_medicamento')
        dosis = request.json.get('dosis')
        observaciones = request.json.get('observaciones')
        periodicidad = request.json.get('periodicidad')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            '''  insert into medicamentos(id_animal,fecha_inicio,fecha_termino,nombre_medicamento,dosis,observaciones,periodicidad)
values(%s,%s,%s,%s,%s,%s,%s) returning id_medicamento''', (id_animal, fecha_inicio, fecha_termino, nombre_medicamento, dosis, observaciones, observaciones))

        result = cursor.fetchone()
        conn.commit()
        print(result)
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "result": result, "message": "Post medicamento funcionando"}), 200
    except:
        return jsonify({"ok": False, "message": "Post medicamento no funcionando"}), 400


post_medicamento.methods = ['POST']
