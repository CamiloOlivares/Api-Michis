from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_medicamentos():
    try:
        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(''' select * from medicamentos''')

        result = cursor.fetchall()

        # print(result[0]['fecha_nacimiento'])
        cursor.close()
        conn.close()

        for res in result:
            res['fecha_inicio'] = str(res['fecha_inicio'])
            res['fecha_termino'] = str(res['fecha_termino'])

        return jsonify({"ok": True, "message": "Get medicamentos funcionando", "medicamentos": result}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get medicamentos no funcionando"}), 400


get_medicamentos.methods = ['GET']


def get_medicamento():
    try:
        id_animal = request.args.get('id_animal')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from medicamentos where id_animal=%s''', (id_animal,))

        result = cursor.fetchall()

        cursor.close()
        conn.close()

        for res in result:
            res['fecha_inicio'] = str(res['fecha_inicio']).split('+')[0]
            res['fecha_termino'] = str(res['fecha_termino']).split('+')[0]

        return jsonify({
            "id_animal": id_animal,
            "ok": True,
            "message": "Get medicamento funcionando",
            "medicamentos":
                result,
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get medicamento no funcionando"}), 400


get_medicamento.methods = ['GET']


def get_medicamento_by_animal():
    try:
        id_animal = request.args.get('id_animal')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from medicamentos where id_animal=%s''', (id_animal,))

        result = cursor.fetchone()

        print(result)
        cursor.close()
        conn.close()

        result['fecha_inicio'] = str(result['fecha_inicio']).split('+')[0]
        result['fecha_termino'] = str(result['fecha_termino']).split('+')[0]

        return jsonify({
            "id_medicamento": id_animal,
            "ok": True,
            "message": "Get medicamento funcionando",
            "medicamento":
                result,
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get medicamento no funcionando"}), 400


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
values(%s,%s,%s,%s,%s,%s,%s) returning id_medicamento''', (id_animal, fecha_inicio, fecha_termino, nombre_medicamento, dosis, observaciones, periodicidad))

        result = cursor.fetchone()
        conn.commit()
        print(result)
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "result": result, "message": "Post medicamento funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Post medicamento no funcionando"}), 400


post_medicamento.methods = ['POST']


def delete_medicamento():
    try:
        id_medicamento = request.json.get('id_medicamento')
        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' delete from medicamentos where id_medicamento=%s''', (id_medicamento,))
        conn.commit()

        # print(result[0]['fecha_nacimiento'])
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Delete medicamentos funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Delete medicamentos no funcionando"}), 400


delete_medicamento.methods = ['DELETE']
