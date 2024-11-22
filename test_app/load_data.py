import json
import os

from model import Benchmark, BenchmarkingList


def load_data_json(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        return data


def parsing_data(filename):
    data = load_data_json(filename)
    validated_data = BenchmarkingList.model_validate(data)
    return validated_data.benchmarking_results

