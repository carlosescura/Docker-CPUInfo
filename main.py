import cpuinfo
import json
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def cpu_info_endpoint():
    try:
        return jsonify(cpuinfo.get_cpu_info()), 200
    except Exception as e:
        # Depending on the requirements, we can expose the error message
        return jsonify(error='There was an error obtaining CPU info'), 500


@app.route('/healthcheck')
def healthcheck_endpoint():
    return jsonify(status='OK'), 200


if __name__ == '__main__':
    # This is the entry point, just run the Flask application
    app.run(host='0.0.0.0', port=8080)
