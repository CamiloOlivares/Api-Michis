from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_animales():
    try:

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(''' select * from animales ''')

        result = cursor.fetchall()

        print(result[0]['fecha_nacimiento'])
        cursor.close()
        conn.close()

        for res in result:

            res['fecha_nacimiento'] = str(res['fecha_nacimiento'])

        return jsonify({"ok": True, "message": "Get animales funcionando", "animales": result}), 200
    except:
        return jsonify({"ok": False, "message": "Get animales no funcionando"}), 400


get_animales.methods = ['GET']


def get_animal():
    try:
        idAnimal = request.args.get('id_animal')

        conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from animales where id_animal=%s''', idAnimal)

        result = cursor.fetchone()

        print(result)
        cursor.close()
        conn.close()

        return jsonify({
            "idAnimal": idAnimal,
            "ok": True,
            "message": "Get animal funcionando",
            "animal":
                result,
        }), 200
    except:
        return jsonify({"ok": False, "message": "Get animal no funcionando"}), 400


get_animales.methods = ['GET']


def post_animales():
    # try:
    nombre = request.json.get('nombre')
    especie = request.json.get('especie')
    sexo = request.json.get('sexo')
    #foto = request.json.get('foto')
    esterilizado = request.json.get('esterilizado')
    raza = request.json.get('raza')
    fecha_nacimiento = request.json.get('fecha_nacimiento')
    color = request.json.get('color')
    observaciones = request.json.get('observaciones')

    print(request.json)

    conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    cursor.execute(
        ''' insert into animales(nombre,especie,raza,sexo,esterilizado,color,fecha_nacimiento,observaciones)
Values(%s,%s,%s,%s,%s,%s,%s,%s) returning id_animal''', (nombre, especie, raza, sexo, esterilizado, color, fecha_nacimiento, observaciones))

    result = cursor.fetchone()
    conn.commit()
    print(result)
    cursor.close()
    conn.close()

    return jsonify({"ok": True, "result": result, "message": "Post animales funcionando"}), 200
    # except:
    #     return jsonify({"ok": False, "message": "Post animal no funcionando"}), 400


post_animales.methods = ['POST']
