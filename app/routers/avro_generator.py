from typing import Dict, List

from fastapi import  APIRouter
from pyscgen.avro._model.record_model import Schema

from app.configuration.getConfig import Config
from app.service.avro_generator import AvroGeneratorService


config = Config()
avro_generator_service: AvroGeneratorService = AvroGeneratorService(config=config)

# fastAPI Instance
router = APIRouter()

# Logger
logger = config.logger


@router.post("/avro/schema/generate", tags=["avro"])
async def avro_generate(docs: List[Dict], name: str = "PyScGenClass", namespace: str = "com.pyscgen.avro"):
    schema: Schema = avro_generator_service.generate_schema(
        docs=docs,
        name=name,
        namespace=namespace
    )
    return schema.as_dict(remove_empty=True)
