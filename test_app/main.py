import os
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from services import get_average_metrics, get_filtered_metrics
from schemas import Benchmark


load_dotenv(find_dotenv())
app = FastAPI()

DEBUG = os.getenv("SUPERBENCHMARK_DEBUG", "False") == "True"


@app.get("/results/average", response_model=Dict[str, float])
async def get_results_average():
    if not DEBUG:
        raise HTTPException(
            status_code=503, detail="The application is not ready to start yet"
        )
    return await get_average_metrics()


@app.get("/results/average/{start_time}/{end_time}", response_model=Dict[str, float])
async def average_over_period_time(start_time: datetime, end_time: datetime):
    if not DEBUG:
        raise HTTPException(
            status_code=503, detail="The application is not ready to start yet"
        )
    return await get_filtered_metrics(start_time, end_time)
