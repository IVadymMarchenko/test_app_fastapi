import json
from model import  BenchmarkingList
import aiofiles
from pydantic import ValidationError

async def load_data_json(filename):
    async with aiofiles.open(filename, mode="r") as file:
        content = await file.read()
        return json.loads(content)


async def parsing_data(filename):
    data =  await load_data_json(filename)
    try:
        validated_data = BenchmarkingList.model_validate(data)
        return validated_data.benchmarking_results
    except ValidationError as e:
        raise ValueError(f"Data validation error:: {e}")



