# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
import datetime
import logging
import os
import socket
import sys  
import json



from flask import Flask, jsonify, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

integrantes = [
    {
        'id': 1,
        'nome': 'Irene Ginani',
        'grupo': 'Pyladies-Natal', 
        'cpf': '09049094049049'
    },
    {
        'id': 2,
        'nome': 'Gabi Cavalcante',
        'grupo': 'Pyladies-Natal', 
        'cpf': '96900200030'
    }
]

grupos = [
    {
        'id': 'Pyladies-Natal'
    },
    {
        'id': 'Pyladies-Salvador'
    }
]

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')
@app.route('/teste.html')
def hell():
    """Return a friendly HTTP greeting."""
    return render_template('teste.html')

@app.route('/v1.0/integrantes/<string:token_id>/<string:cliente_id>', methods=['GET'])
def get_integrantes(token_id, cliente_id):

    data =  { "token-id": token_id, "server-appspot": "pyladies-info-1544364856514",
              "client-appspot": cliente_id, "service-name": "Vizualizar Integrantes"}

    response = requests.post("https://orchestrator-224010.appspot.com/explore/token/validate", data=json.dumps(data))
    if response == "<Response [404]>" or response == "<Response [502]>":
        return jsonify({'ERROR': "erro de validacao"})
    return jsonify({'integrantes': integrantes})
    
@app.route('/v1.0/integrantes', methods=['POST'])
def criar_integrantes():
    if not request.json or not 'cpf' in request.json:
        abort(400)
    integrante = {
        'id': integrantes[-1]['id'] + 1,
        'nome': request.json['nome'],
        'cpf': request.json['cpf'],
        'grupo': request.json['grupo']
    }
    integrantes.append(integrante)
    return jsonify({'integrantes': integrantes}), 201

@app.route('/v1.0/integrantes/<int:integrante_id>', methods=['PUT'])
def atualizar_integrante(integrante_id):
    integrante = [integrante for integrante in integrantes if integrante['id'] == integrante_id]
    if len(integrante) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'cpf' in request.json and type(request.json['cpf']) != unicode:
        abort(400)
    if 'nome' in request.json and type(request.json['nome']) is not unicode:
        abort(400)
    if 'grupo' in request.json and type(request.json['grupo']) is not unicode:
        abort(400)
    integrantes[0]['cpf'] = request.json.get('cpf', integrante[0]['cpf'])
    integrantes[0]['grupo'] = request.json.get('grupo', integrante[0]['grupo'])
    integrantes[0]['nome'] = request.json.get('nome', integrante[0]['nome'])
    return jsonify({'integrantes': integrantes[0]})

@app.route('/v1.0/integrantes/<int:integrante_id>', methods=['DELETE'])
def apagar_integrante(integrante_id):
    integrante = [integrante for integrante in integrantes if integrante['id'] == integrante_id]
    if len(integrante) == 0:
        abort(404)
    integrantes.remove(integrante[0])
    return jsonify({'result': True})

@app.route('/v1.0/grupos/<string:token_id>/<string:cliente_id>', methods=['GET'])
def get_grupos(token_id, cliente_id):

    data =  { "token-id": token_id, "server-appspot": "pyladies-info-1544364856514",
              "client-appspot": cliente_id, "service-name": "Vizualizar Grupos"}

    response = requests.post("https://orchestrator-224010.appspot.com/explore/token/validate", data=json.dumps(data))

    if response == "<Response [404]>" or response == "<Response [502]>":
        return jsonify({'ERROR': "erro de validacao"})
    return jsonify({'grupos': grupos})

@app.route('/v1.0/grupos/', methods=['POST'])
def criar_grupos():
    if not request.json or not 'id' in request.json:
        abort(400)
    grupo = {
        'id': request.json['id']
    }
    grupos.append(grupo)
    return jsonify({'grupos': grupos}), 201

@app.route('/v1.0/grupos/<int:grupo_id>', methods=['PUT'])
def atualizar_grupo(integrante_id):
    grupo = [grupo for grupo in grupos if grupo['id'] == grupo_id]
    if len(grupo) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'id' in request.json and type(request.json['id']) != unicode:
        abort(400)
    grupos[0]['id'] = request.json.get('id', grupo[0]['id'])
    return jsonify({'grupos': grupos[0]})

@app.route('/v1.0/integrantes/<int:grupo_id>', methods=['DELETE'])
def apagar_grupo(integrante_id):
    grupo = [grupo for grupo in grupos if grupo['id'] == grupo_id]
    if len(grupo) == 0:
        abort(404)
    grupos.remove(grupo[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8081, debug=True)
# [END gae_python37_app]
