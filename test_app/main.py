from datetime import datetime
import os
from fastapi import FastAPI, HTTPException
from load_data import parsing_data
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
app = FastAPI()

DEBUG = os.getenv("SUPERBENCHMARK_DEBUG", "False") == "True"


@app.get("/results/average")
async def get_results_average():
    if not DEBUG:
        raise HTTPException(
            status_code=500, detail="the application is not ready for start yet"
        )
    data = await parsing_data("test_database.json")
    average_value_token_count = sum(result.token_count for result in data)
    average_value_time_to_first_token = sum(
        result.time_to_first_token for result in data
    ) / len(data)
    average_value_time_per_output_token = sum(
        result.time_per_output_token for result in data
    ) / len(data)
    average_value_total_generation_time = sum(
        result.total_generation_time for result in data
    ) / len(data)
    average_value_prompt_text = sum(len(result.prompt_text) for result in data) / len(
        data
    )
    average_value_generated_text = sum(
        len(result.generated_text) for result in data
    ) / len(data)

    return {
        "average_value_token_count": average_value_token_count,
        "average_value_time_to_first_token": average_value_time_to_first_token,
        "average_value_time_per_output_token": average_value_time_per_output_token,
        "average_value_total_generation_time": average_value_total_generation_time,
        "average_value_prompt_text": average_value_prompt_text,
        "average_value_generated_text": average_value_generated_text,
    }


@app.get("/results/average/{start_time}/{end_time}")
async def average_over_period_time(start_time: datetime, end_time: datetime):
    if not DEBUG:
        raise HTTPException(
            status_code=500, detail="the application is not ready for start yet"
        )
    data = await parsing_data("test_database.json")
    filtered_data = [
        result for result in data if start_time <= result.timestamp <= end_time
    ]
    average_value_token_count = sum(result.token_count for result in filtered_data)
    average_value_time_to_first_token = sum(
        result.time_to_first_token for result in filtered_data
    ) / len(filtered_data)
    average_value_time_per_output_token = sum(
        result.time_per_output_token for result in filtered_data
    ) / len(filtered_data)
    average_value_total_generation_time = sum(
        result.total_generation_time for result in filtered_data
    ) / len(filtered_data)
    average_value_prompt_text = sum(
        len(result.prompt_text) for result in filtered_data
    ) / len(filtered_data)
    return {
        "average_value_token_count": average_value_token_count,
        "average_value_time_to_first_token": average_value_time_to_first_token,
        "average_value_time_per_output_token": average_value_time_per_output_token,
        "average_value_total_generation_time": average_value_total_generation_time,
        "average_value_prompt_text": average_value_prompt_text,
    }
