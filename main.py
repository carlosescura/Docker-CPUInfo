import json
from flask import Flask, jsonify
import re

app = Flask(__name__)


_re_processor = re.compile(r'processor\s+: (\d+)')


class CPU(object):
    def __init__(self):
        self.vendor_id = ''
        self.family = ''
        self.model = ''
        self.model_name = ''
        self.stepping = ''
        self.mhz = ''
        self.cache_size = ''
        self.physical_id = ''
        self.core_id = ''
        self.cores = ''
        self.siblings = ''
        self.flags = ''


def get_num_cpu_sockets(processors):
    physical_ids = []
    for k, v in processors.items():
        if v['physical_id'] not in physical_ids:
            physical_ids.append(v['physical_id'])

    return len(physical_ids)


def get_num_total_threads(processors):
    threads = 0
    physical_ids = []
    for k, v in processors.items():
        if v['physical_id'] not in physical_ids:
            siblings_in_cpu = int(v['siblings'])
            threads += siblings_in_cpu
    print(threads)
    return threads


def calculate_core_stats(processors):
    cores = len(processors)
    real = get_num_cpu_sockets(processors)
    total = get_num_total_threads(processors)

    processors['cores'] = cores
    processors['real'] = real
    processors['total'] = total

    return processors


def get_cpuinfo():
    processors = {}
    current_processor = None
    with open('/proc/cpuinfo') as f:
        for line in f.readlines():
            m = re.match(r'processor\s+: (\d+)', line)
            if m:
                current_processor = CPU()
                processors[m.group(1)] = current_processor

            m = re.match(r'vendor_id\s+: (.*)', line)
            if m:
                current_processor.vendor_id = m.group(1)

            m = re.match(r'family\s+: (.*)', line)
            if m:
                current_processor.family = m.group(1)

            m = re.match(r'model\s+: (.*)', line)
            if m:
                current_processor.model = m.group(1)

            m = re.match(r'model name\s+: (.*)', line)
            if m:
                current_processor.model_name = m.group(1)

            m = re.match(r'stepping\s+: (.*)', line)
            if m:
                current_processor.stepping = m.group(1)

            m = re.match(r'cpu MHz\s+: (.*)', line)
            if m:
                current_processor.mhz = m.group(1)

            m = re.match(r'cache size\s+: (.*)', line)
            if m:
                current_processor.cache_size = m.group(1)

            m = re.match(r'physical id\s+: (.*)', line)
            if m:
                current_processor.physical_id = m.group(1)

            m = re.match(r'core id\s+: (.*)', line)
            if m:
                current_processor.core_id = m.group(1)

            m = re.match(r'cpu cores\s+: (.*)', line)
            if m:
                current_processor.cores = m.group(1)

            m = re.match(r'siblings\s+: (.*)', line)
            if m:
                current_processor.siblings = m.group(1)

            m = re.match(r'flags\s+: (.*)', line)
            if m:
                flags = m.group(1).split()
                current_processor.flags = flags

    if len(processors):
        for p in processors:
            processors[p] = processors[p].__dict__
        return calculate_core_stats(processors)

    return processors


@app.route('/')
def cpu_info_endpoint():
    try:
        # return jsonify(cpuinfo.get_cpu_info()), 200
        return jsonify(get_cpuinfo()), 200
    except Exception as e:
        # Depending on the requirements, we can expose the error message
        return jsonify(error='There was an error obtaining CPU info'), 500


@app.route('/healthcheck')
def healthcheck_endpoint():
    return jsonify(status='OK'), 200


if __name__ == '__main__':
    # This is the entry point, just run the Flask application
    app.run(host='0.0.0.0', port=8080)
