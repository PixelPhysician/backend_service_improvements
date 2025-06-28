"""
Flask backend service for digital biomarker data collection.
"""

import logging
import os
import random
import json
import psutil

from flask import request, Flask, jsonify, make_response
from flask_httpauth import HTTPBasicAuth

import datastructure

app = Flask(__name__)
auth = HTTPBasicAuth()

# Basic auth setup
users = {
    "user": "password"
}

@auth.verify_password
def verify_password(username, password):
    """Verifies the basic auth credentials."""
    return username if users.get(username) == password else None

def load_environment():
    """Loads environment variables from file."""
    try:
        env_file = os.environ['WORKING_ENV']
    except KeyError:
        env_file = 'dev_env.json'

    with open(env_file) as file:
        env_values = json.loads(file.read())

    logging.info("Loaded environment config: %s", env_file)
    return env_values

big_data = []

@app.route('/memory', methods=['GET'])
def memory():
    """Simulates memory consumption and returns memory usage."""
    logging.info("Memory endpoint accessed.")
    for _ in range(0, 1000000):
        big_data.append(random.random())

    process = psutil.Process()
    memory_usage = process.memory_info().rss / (1024.0 ** 2)
    logging.info("Memory used: %.2f MB", memory_usage)
    return json.dumps({'size': len(big_data), 'memory': memory_usage})

@app.route('/', methods=['GET'])
@auth.login_required
def index():
    """Returns project metadata."""
    logging.info("Index route accessed with authentication.")
    return json.dumps({'name': 'David',
                       'mail': 'david.herzig@roche.com',
                       'System': 'Digital Biomarker Course Project',
                       'Server Component': 'v1_0_0',
                       'Date': '7-Apr-2025'})

@app.route('/experiment', methods=['POST', 'GET'])
def experiment_action():
    """Handles creation and retrieval of experiments."""
    logging.info('Experiment endpoint called [%s]', request.method)
    data_storage = datastructure.DataStorage()

    if request.method == 'POST':
        body = request.get_json()
        assert 'name' in body, "Missing 'name' in request body"
        experiment_obj = datastructure.Experiment(body['name'])
        data_storage.add_experiment(experiment_obj)
        logging.info("Experiment created: %s", experiment_obj.id)
        return jsonify(experiment_obj.__dict__)

    experiment_id = request.args.get('id')
    result = data_storage.get_experiment(experiment_id)
    if result is None:
        logging.warning("Experiment not found: %s", experiment_id)
        return make_response(jsonify('experiment not found'), 404)
    return make_response(jsonify(result.__dict__), 200)

@app.route('/patient', methods=['POST', 'GET'])
def patient_action():
    """Handles creation and retrieval of patients."""
    logging.info('Patient endpoint called [%s]', request.method)
    data_storage = datastructure.DataStorage()

    if request.method == 'POST':
        body = request.get_json()
        assert 'name' in body, "Missing 'name' in request body"
        patient_obj = datastructure.Patient(body['name'])
        data_storage.add_patient(patient_obj)
        logging.info("Patient created: %s", patient_obj.id)
        return jsonify(patient_obj.__dict__)

    patient_id = request.args.get('id')
    result = data_storage.get_patient(patient_id)
    if result is None:
        logging.warning("Patient not found: %s", patient_id)
        return make_response(jsonify('patient not found'), 404)
    return make_response(jsonify(result.__dict__), 200)

@app.route('/patients', methods=['GET'])
def patients_action():
    """Returns all patient data."""
    logging.info("Listing all patients.")
    data_storage = datastructure.DataStorage()
    return json.dumps(data_storage.patients, cls=datastructure.PatientEncoder)

@app.route('/experiments', methods=['GET'])
def experiments_action():
    """Returns all experiment data."""
    logging.info("Listing all experiments.")
    data_storage = datastructure.DataStorage()
    return json.dumps(data_storage.experiments, cls=datastructure.ExperimentEncoder)

@app.route('/store', methods=['POST'])
def store_data():
    """Triggers data persistence to file."""
    logging.info("Storing all data to disk.")
    data_storage = datastructure.DataStorage()
    data_storage.store_data()
    return make_response(jsonify("True"), 200)

@app.route('/upload', methods=['POST'])
def upload_data():
    """Uploads a new datapoint and stores it in memory."""
    logging.info("Upload endpoint called.")
    data_storage = datastructure.DataStorage()
    body = request.get_json()

    assert 'patientId' in body, "Missing 'patientId'"
    assert 'experimentId' in body, "Missing 'experimentId'"

    patient_id = body['patientId']
    experiment_id = body['experimentId']
    data_obj = datastructure.DataPoint(patient_id, experiment_id, body)

    data_storage.add_data(data_obj)
    logging.info("Data uploaded for patient %s in experiment %s", patient_id, experiment_id)
    return make_response('', 200)

if __name__ == '__main__':
    print('Starting service...')
    logging.basicConfig(filename="backend_service.log", encoding='utf-8', level=logging.INFO)
    logging.debug('Application started...')
    env_variables = load_environment()
    assert env_variables is not None
    data_storage = datastructure.DataStorage()
    data_storage.load_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
