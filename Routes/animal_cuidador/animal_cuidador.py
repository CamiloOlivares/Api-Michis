from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def post_animales_cuidador():
    try:
        nombre = request.json.get('nombre')
        especie = request.json.get('especie')
        sexo = request.json.get('sexo')
        #foto = request.json.get('foto')
        esterilizado = request.json.get('esterilizado')
        raza = request.json.get('raza')
        fecha_nacimiento = request.json.get('fecha_nacimiento')
        color = request.json.get('color')
        observaciones = request.json.get('observaciones')
        correo = request.json.get('correo')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' insert into animales(nombre,especie,raza,sexo,esterilizado,color,fecha_nacimiento,observaciones)
    Values(%s,%s,%s,%s,%s,%s,%s,%s) returning id_animal''', (nombre, especie, raza, sexo, esterilizado, color, fecha_nacimiento, observaciones))

        result = cursor.fetchone()

        id_animal = result['id_animal']

        cursor.execute(
            ''' CALL SP_VINCULA_ANIMAL_A_CUIDADOR(%s, %s);''', (id_animal, correo))
        print(result)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "result": result, "message": "Post animales cuidadores funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Post animal  cuidadores no funcionando"}), 400


post_animales_cuidador.methods = ['POST']


def asign_animal_cuidador():
    try:
        id_animal = request.json.get('id_animal')
        correo = request.json.get('correo')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' CALL SP_VINCULA_ANIMAL_A_CUIDADOR(%s, %s);''', (id_animal, correo))

        #result = cursor.fetchone()

        #id_animal = result['id_animal']
        # print(result)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Asign animales cuidadores funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Asign animal  cuidadores no funcionando"}), 400


asign_animal_cuidador.methods = ['POST']


def get_cuidadores_animal():
    try:
        id_animal = request.args.get('id_animal')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select *
from Cuidadores, Animal_Cuidador
where Cuidadores.id_cuidador=Animal_Cuidador.id_cuidador and Animal_Cuidador.id_animal=%s''', (id_animal,))

        result = cursor.fetchall()

        #id_animal = result['id_animal']
        # print(result)
        for res in result:
            res['fecha_ingreso'] = str(res['fecha_ingreso']).split('+')[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "result": result, "message": "Get cuidadores animal funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Get cuidadores animal no funcionando"}), 400


get_cuidadores_animal.methods = ['GET']


def delete_relacion_animal_cuidador():
    try:
        id_animal = request.json.get('id_animal')
        id_cuidador = request.json.get('id_cuidador')

        print(request.json)

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' delete from Animal_cuidador where id_animal=%s and id_cuidador=%s''', (id_animal, id_cuidador))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"ok": True, "message": "Delete relacion cuidador animal funcionando"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e), "message": "Delete relacion cuidador animal no funcionando"}), 400


delete_relacion_animal_cuidador.methods = ['POST']
