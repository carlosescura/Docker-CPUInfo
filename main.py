import cpuinfo
import json
from flask import Flask, jsonify


# Generate the Flask server instance and name it "app" as a general convention
app = Flask(__name__)


@app.route('/')
def status_endpoint():
    # Just return cpuinfo and a 200 status code
    try:
        return jsonify(cpuinfo.get_cpu_info()), 200
    except Exception as e:
        # Depending on the requirements, we can expose the error message
        return jsonify(error='There was an error obtaining CPU info'), 500


if __name__ == '__main__':
    # This is the entry point, just run the Flask application
    app.run(host='0.0.0.0', port=8080)
