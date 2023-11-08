import json
from typing import Dict, List

from fastapi import APIRouter

from app.configuration.getConfig import Config
from app.service.data_generator import DataGeneratorService
config = Config()
data_generator_service: DataGeneratorService = DataGeneratorService(config=config)

# fastAPI Instance
router = APIRouter()

# Logger
logger = config.logger


@router.post("/avro/data/generate", tags=["avro"])
async def generate_data(avro_schema: dict, number_of_records: int = 5) -> List[Dict]:
    data: List[Dict] = data_generator_service.generate(avro_schema=avro_schema, number_of_recors=number_of_records)
    return data
