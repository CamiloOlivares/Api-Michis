from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json
import os
from datetime import datetime, timedelta, date

DATABASE = os.getenv("DATABASE")


def get_eventos_plan():
    # try:
    id_plan_alimentacion = request.args.get('id_plan_alimentacion')

    conn = pg2.connect(DATABASE, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    cursor.execute(
        ''' select * from planes_alimentacion where id_plan_alimentacion=%s''', id_plan_alimentacion)

    result = cursor.fetchone()

    print(result)
    cursor.close()
    conn.close()

    time = result['periodicidad'].split()[0]

    timeMetric = result['periodicidad'].split()[1]

    print("el intervalo es"+time+"  "+timeMetric)

    plan_date = result['fecha_inicio']
    dates = []
    dates.append(str(plan_date).split('+')[0])
    i = 0
    while i < 6:
        plan_date = plan_date + timedelta(hours=int(time))
        dates.append(str(plan_date).split('+')[0])
        i = i + 1
    print(datetime.now())
    future_dates = [d for d in dates if datetime.strptime(
        d, "%Y-%m-%d %H:%M:%S").date() > datetime.now().date()]
    print(future_dates)
    next_date = min(future_dates, key=lambda s:
                    datetime.strptime(
                        s, "%Y-%m-%d %H:%M:%S").date()-datetime.now().date()
                    )

    print(next_date)
    return jsonify({
        "id_plan_alimentacion": id_plan_alimentacion,
        "ok": True,
        "message": "Get evento plan alimentacion funcionando",
        "plan_alimentacion_dates":
            dates,
        "next_event": next_date,
        "plan_alimentacion": result
    }), 200
    # except:
    #     return jsonify({"ok": False, "message": "Get evento plan alimentacion no funcionando"}), 400


get_eventos_plan.methods = ['GET']


def get_eventos_medicacion():
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

        time = result['periodicidad'].split()[0]

        timeMetric = result['periodicidad'].split()[1]

        print("el intervalo es"+time+"  "+timeMetric)

        plan_date = result['fecha_inicio']
        dates = []
        dates.append(str(plan_date).split('+')[0])
        i = 0
        while plan_date < result['fecha_termino']:
            if(timeMetric == 'horas'):
                plan_date = plan_date + timedelta(hours=int(time))
            elif(timeMetric == 'dias'):
                plan_date = plan_date + timedelta(days=int(time))
            elif(timeMetric == 'semanas'):
                plan_date = plan_date + timedelta(weeks=int(time))

            dates.append(str(plan_date).split('+')[0])
            i = i + 1
        print(datetime.now())
        future_dates = [d for d in dates if datetime.strptime(
            d, "%Y-%m-%d %H:%M:%S").date() > datetime.now().date()]
        print(future_dates)
        next_date = min(future_dates, key=lambda s:
                        datetime.strptime(
                            s, "%Y-%m-%d %H:%M:%S").date()-datetime.now().date()
                        )

        print(next_date)
        return jsonify({
            "id_plan_alimentacion": id_medicamento,
            "ok": True,
            "message": "Get evento medicamento funcionando",
            "medicamento_dates":
                dates,
            "next_event": next_date,
            "medicamento": result
        }), 200
    except:
        return jsonify({"ok": False, "message": "Get evento plan alimentacion no funcionando"}), 400


get_eventos_medicacion.methods = ['GET']
