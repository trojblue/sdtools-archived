import json

import sdtools
import sdtools.sdt
from sdtools.benchmark import run_benchmarks


def do_test_from_json():
    json_path = "D:\CSC3\sdtools\out\\23.01.02_0826__do_random_benchmark\\config_23.01.02_0826.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        benchmark_json = json.loads(f.read())

    sdt = sdtools.sdt.SDTools()

    run_benchmarks(sdt, benchmark_json, "JSON_BENCH")



if __name__ == '__main__':
    do_test_from_json()