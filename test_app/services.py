from datetime import datetime
from typing import List, Dict
from data_loader import parse_benchmark_data
from schemas import Benchmark


# Загал функ розрах серед знач
def calculate_averages_values(data: List[Benchmark]) -> Dict[str, float]:
    if not data:
        return {
            "average_value_token_count": 0.0,
            "average_value_time_to_first_token": 0.0,
            "average_value_time_per_output_token": 0.0,
            "average_value_total_generation_time": 0.0,
            "average_value_prompt_text": 0.0,
            "average_value_generated_text": 0.0,
        }
    return {
        "average_value_token_count": sum(result.token_count for result in data)
        / len(data),
        "average_value_time_to_first_token": sum(
            result.time_to_first_token for result in data
        )
        / len(data),
        "average_value_time_per_output_token": sum(
            result.time_per_output_token for result in data
        )
        / len(data),
        "average_value_total_generation_time": sum(
            result.total_generation_time for result in data
        )
        / len(data),
        "average_value_prompt_text": sum(len(result.prompt_text) for result in data)
        / len(data),
        "average_value_generated_text": sum(
            len(result.generated_text) for result in data
        )
        / len(data),
    }


# Отрим всіх серед знач
async def get_average_metrics() -> Dict[str, float]:
    data = await parse_benchmark_data("test_database.json")
    return calculate_averages_values(data)


# Отрим середніх значень за заданий період
async def get_filtered_metrics(
    start_time: datetime, end_time: datetime
) -> Dict[str, float]:
    data = await parse_benchmark_data("test_database.json")
    filtered_data = [
        result for result in data if start_time <= result.timestamp <= end_time
    ]
    return calculate_averages_values(filtered_data)
