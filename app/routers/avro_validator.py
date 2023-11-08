from typing import Dict, List, Any

from fastapi import APIRouter

from app.configuration.getConfig import Config
from app.model.validation_model import ValidationModel
from app.service.avro_validator import AvroValidatorService
config = Config()
avro_validator_service: AvroValidatorService = AvroValidatorService(config=config)

# fastAPI Instance
router = APIRouter()

# Logger
logger = config.logger


@router.post("/avro/schema/validate", tags=["avro"], response_model=ValidationModel)
async def validate_avro_schema(avro_schema: dict, records: List[dict]) -> bool:
    validation_result, message = avro_validator_service.validate(avro_schema=avro_schema, records=records)
    return {"validation_result": validation_result, "message": message}
