import json
import os

from model import Benchmark
import aiofiles
from pydantic import ValidationError


async def load_data_json(filename):
    async with aiofiles.open(filename, mode="r") as file:
        data = json.loads(await file.read())
        return data


async def parsing_data(filename):
    data = await load_data_json(filename)
    try:
        validated_data = [
            Benchmark.model_validate(benchmark_data)
            for benchmark_data in data.get("benchmarking_results", [])
        ]
        return validated_data
    except ValidationError as e:
        raise ValueError(f"Data validation error:: {e}")
