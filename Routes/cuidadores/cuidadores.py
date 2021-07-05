from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os
from datetime import datetime

DATABASE = os.getenv("DATABASE")


def post_cuidador():
    try:
        nombre = request.json.get('nombre')
        password = request.json.get('password')
        fecha_ingreso = request.json.get('fecha_ingreso')
        correo = request.json.get('correo')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            '''  insert into cuidadores(nombre,fecha_ingreso,correo,password) values(%s,%s,%s,%s) returning id_cuidador''', (nombre, fecha_ingreso, correo, password))

        result = cursor.fetchone()
        conn.commit()
        print(result['id_cuidador'])
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Post cuidador funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Post cuidador no funcionando"}), 400


post_cuidador.methods = ['POST']


def get_cuidadores():
    try:
        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(''' select * from cuidadores''')

        result = cursor.fetchall()

        # print(result[0]['fecha_nacimiento'])
        cursor.close()
        conn.close()

        for res in result:
            res['fecha_ingreso'] = str(res['fecha_ingreso'])

        return jsonify({"ok": True, "message": "Get cuidadores funcionando", "cuidadores": result}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get cuidadores no funcionando"}), 400


def get_cuidador_login():
    try:
        correo = request.json.get('correo')
        password = request.json.get('password')
        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from FN_ANIMALES_CUIDADOR(%s,%s)''', (correo, password))

        result = cursor.fetchone()
        if result:
            print(result)
            cursor.close()
            conn.close()

            # for res in result:
            result['fecha_ingreso'] = str(result['fecha_ingreso'])

            return jsonify({"ok": True, "message": "Get cuidador login funcionando", "result": result}), 200
        else:
            return Exception("No se encuentra el usuario")
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get cuidador login no funcionando"}), 400


get_cuidador_login.methods = ['POST']

def get_cuidador_linea_temporal():
    try:
        id_cuidador = request.args.get('id_cuidador')
        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from FN_GET_LINEA_TEMPORAL_CUIDADOR(%s)''', (id_cuidador,))

        result = cursor.fetchall()
        if result:
            eventillos = []
            for el in result:
                for ev in el['eventos']:
                    eventillos.append({ 
                        "id_animal":el['id_animal'],
                        "nombre_animal":el['nombre_animal'],
                        "tipo_evento":el['tipo_evento'],
                        "id_plan":el['id'],
                        "nombre_plan": el['nombre'],
                        "dosis":el['dosis'],
                        "fecha": ev['fecha'],
                        "cumplido": ev['cumplido'],
                        "observaciones": ev['observaciones']
                    }) 
            cursor.close()
            conn.close()
            #print(eventillos)
            eventillos.sort(key = lambda x:x["fecha"])
            def removeduplicate(it):
                seen = []
                for x in it:
                    if x not in seen:
                        yield x
                        seen.append(x)
         
            return jsonify({"ok": True, "message": "Get linea temporal de cuidador funcionando", "result": list(removeduplicate(eventillos))}), 200
        else:
            return Exception("No se encuentra el usuario")
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get linea temporal de cuidador no funcionando"}), 400


get_cuidador_linea_temporal.methods = ['GET']


def delete_cuidador():
    try:
        correo = request.json.get('correo')
        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' delete from cuidadores where correo=%s''', (correo,))
        conn.commit()

        # print(result[0]['fecha_nacimiento'])
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Delete cuidadores funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Delete cuidadores no funcionando"}), 400


delete_cuidador.methods = ['DELETE']
