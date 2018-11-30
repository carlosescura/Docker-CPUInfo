import json
from flask import Flask, jsonify
import re

app = Flask(__name__)


# Precompile all regex to obtain a performance increase
_re_processor = re.compile(r'processor\s+: (\d+)')
_re_vendor_id = re.compile(r'vendor_id\s+: (.*)')
_re_family = re.compile(r'family\s+: (.*)')
_re_model = re.compile(r'model\s+: (.*)')
_re_model_name = re.compile(r'model name\s+: (.*)')
_re_stepping = re.compile(r'stepping\s+: (.*)')
_re_cpu_MHz = re.compile(r'cpu MHz\s+: (.*)')
_re_cache_size = re.compile(r'cache size\s+: (.*)')
_re_physical_id = re.compile(r'physical id\s+: (.*)')
_re_core_id = re.compile(r'core id\s+: (.*)')
_re_cpu_cores = re.compile(r'cpu cores\s+: (.*)')
_re_siblings = re.compile(r'siblings\s+: (.*)')
_re_flags = re.compile(r'flags\s+: (.*)')


class Processor(object):
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

    def toDict(self):
        return self.__dict__


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
            m = _re_processor.match(line)
            if m:
                current_processor = Processor()
                processors[m.group(1)] = current_processor

            m = _re_vendor_id.match(line)
            if m:
                current_processor.vendor_id = m.group(1)

            m = _re_family.match(line)
            if m:
                current_processor.family = m.group(1)

            m = _re_model.match(line)
            if m:
                current_processor.model = m.group(1)

            m = _re_model_name.match(line)
            if m:
                current_processor.model_name = m.group(1)

            m = _re_stepping.match(line)
            if m:
                current_processor.stepping = m.group(1)

            m = _re_cpu_MHz.match(line)
            if m:
                current_processor.mhz = m.group(1)

            m = _re_cache_size.match(line)
            if m:
                current_processor.cache_size = m.group(1)

            m = _re_physical_id.match(line)
            if m:
                current_processor.physical_id = m.group(1)

            m = _re_core_id.match(line)
            if m:
                current_processor.core_id = m.group(1)

            m = _re_cpu_cores.match(line)
            if m:
                current_processor.cores = m.group(1)

            m = _re_siblings.match(line)
            if m:
                current_processor.siblings = m.group(1)

            m = _re_flags.match(line)
            if m:
                current_processor.flags = m.group(1).split()

    if len(processors):
        for p in processors:
            processors[p] = processors[p].toDict()
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
