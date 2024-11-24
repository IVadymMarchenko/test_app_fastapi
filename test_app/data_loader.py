import json
import aiofiles
from schemas import Benchmark
from pydantic import ValidationError
from fastapi import HTTPException


async def load_data_from_json(filename: str) -> dict:
    try:
        async with aiofiles.open(filename, mode="r") as file:
            return json.loads(await file.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, detail=f"Failed to decode JSON in {filename}"
        )


async def parse_benchmark_data(filename: str) -> list[Benchmark]:
    data = await load_data_from_json(filename)
    try:
        return [
            Benchmark.model_validate(benchmark_data)
            for benchmark_data in data.get("benchmarking_results", [])
        ]
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Data validation error: {e}")
