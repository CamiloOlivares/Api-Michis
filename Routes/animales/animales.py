from flask import Flask, request, jsonify
import psycopg2 as pg2
from psycopg2.extras import RealDictCursor
import json


def get_animales():
    return jsonify({"ok": True, "message": "Api animales funcionando"}), 200
