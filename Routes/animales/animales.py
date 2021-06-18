from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os

DATABASE = os.getenv("DATABASE")


def get_animales():
    print(DATABASE)
    conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    cursor.execute(''' select * from animales ''')

    result = cursor.fetchall()

    print(result[0]['fecha_nacimiento'])

    for res in result:

        res['fecha_nacimiento'] = str(res['fecha_nacimiento'])

    cursor.close()
    conn.close()

    return jsonify({"ok": True, "message": "Api animales funcionando", "result": result}), 200


get_animales.methods = ['GET']


def get_animal():
    try:
        idAnimal = request.args.get('id')
        return jsonify({
            "idAnimal": idAnimal,
            "ok": True,
            "message": "Api animales get funcionando",
            "animal": {
                "nombre": "perrito",
                "especie": "gato",
                "sexo": "macho",
                "esterilizado": True,
                "raza": "Siames",
                "fechaNac": "17-06-2021",
                "color": "azul",
                "observaciones": "esta mamadisimo",
                "foto": "https://estaticos.muyinteresante.es/media/cache/1140x_thumb/uploads/images/gallery/593561e75bafe823cd3c9869/gato-azul-ruso_0.jpg"
            },
        }), 200
    except:
        return 400


get_animales.methods = ['GET']


def post_animales():
    try:
        nombre = request.json.get('nombre')
        return jsonify({"ok": True, "nombre": nombre, "message": "Post animales funcionando"}), 200
    except:
        return 400


post_animales.methods = ['POST']
