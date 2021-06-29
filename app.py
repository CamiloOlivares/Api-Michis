#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_cors import CORS
from Routes.animales import animales
from Routes.medicamentos import medicamentos
from Routes.planes_alimentacion import planes_alimentacion
from Routes.registros_plan_alimentacion import registro_plan_alimentacion
from Routes.medicamento_suministrado import medicamento_suministrado
from Routes.eventos import eventos
from Routes.registros_peso import registros_peso
from Routes.cuidadores import cuidadores
from Routes.animal_cuidador import animal_cuidador

app = Flask(__name__)
cors = CORS(app)

# animales
app.add_url_rule('/animales', view_func=animales.get_animales)
app.add_url_rule('/animal', view_func=animales.get_animal)
app.add_url_rule('/animal', view_func=animales.delete_animal)
app.add_url_rule('/animal', view_func=animales.post_animales)
# medicamentos
app.add_url_rule('/medicamentos', view_func=medicamentos.get_medicamentos)
app.add_url_rule('/medicamento', view_func=medicamentos.get_medicamento)
app.add_url_rule('/medicamento_by_animal',
                 view_func=medicamentos.get_medicamento_by_animal)
app.add_url_rule('/medicamento', view_func=medicamentos.post_medicamento)
# plan de alimentacion
app.add_url_rule('/planes_alimentacion',
                 view_func=planes_alimentacion.get_all_planes_alimentacion)
app.add_url_rule('/plan_alimentacion',
                 view_func=planes_alimentacion.get_planes_alimentacion)
app.add_url_rule('/plan_alimentacion',
                 view_func=planes_alimentacion.post_planes_alimentacion)
# registro plan alimentacion
app.add_url_rule('/registro_plan_alimentacion',
                 view_func=registro_plan_alimentacion.get_registro_plan)
app.add_url_rule('/registro_plan_alimentacion',
                 view_func=registro_plan_alimentacion.post_registro_plan)
# medicamentos suministrados
app.add_url_rule('/medicamentos_suministrados',
                 view_func=medicamento_suministrado.get_medicamento_suministrado)
app.add_url_rule('/medicamentos_suministrados',
                 view_func=medicamento_suministrado.post_medicamento_suministrado)
# eventos
app.add_url_rule('/eventos_plan_alimentacion',
                 view_func=eventos.get_eventos_plan)
app.add_url_rule('/eventos_medicamento',
                 view_func=eventos.get_eventos_medicacion)
app.add_url_rule('/eventos_alimentacion_animal',
                 view_func=eventos.get_eventos_alimentacion_animal)
app.add_url_rule('/eventos_medicacion_animal',
                 view_func=eventos.get_eventos_medicacion_animal)
app.add_url_rule('/eventos',
                 view_func=eventos.get_todos_eventos_animal)
# registro peso
app.add_url_rule('/registros_peso',
                 view_func=registros_peso.get_registros_peso)
app.add_url_rule('/registro_peso',
                 view_func=registros_peso.post_registro_peso)
app.add_url_rule('/eventos_medicamento',
                 view_func=registros_peso.get_registro_peso)
app.add_url_rule('/registro_peso/get_by_dates',
                 view_func=registros_peso.get_pesos_intervalo)
app.add_url_rule('/registro_last_peso',
                 view_func=registros_peso.get_last_registro_peso)
# cuidador
app.add_url_rule('/cuidador',
                 view_func=cuidadores.post_cuidador)
app.add_url_rule('/cuidadores',
                 view_func=cuidadores.get_cuidadores)
app.add_url_rule('/login',
                 view_func=cuidadores.get_cuidador_login)
app.add_url_rule('/cuidador',
                 view_func=cuidadores.delete_cuidador)
# animal cuidador
app.add_url_rule('/animal_cuidador',
                 view_func=animal_cuidador.post_animales_cuidador)
app.add_url_rule('/asigna_animal_cuidador',
                 view_func=animal_cuidador.asign_animal_cuidador)
app.add_url_rule('/get_cuidadores_animal',
                 view_func=animal_cuidador.get_cuidadores_animal)
app.add_url_rule('/delete_relacion_animal_cuidador',
                 view_func=animal_cuidador.delete_relacion_animal_cuidador)

if __name__ == '__main__':
    #app.run(debug=True,host='192.168.0.50', port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)
