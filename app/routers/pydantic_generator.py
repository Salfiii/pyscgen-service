from typing import Dict, List, AnyStr

from fastapi import APIRouter

from app.configuration.getConfig import Config
from app.service.pydantic_generator import PydanticGeneratorService


config = Config()
avro_generator_service: PydanticGeneratorService = PydanticGeneratorService(config=config)

# fastAPI Instance
router = APIRouter()

# Logger
logger = config.logger


@router.post("/pydantic/schema/generate", tags=["pydantic"], response_model=AnyStr)
async def avro_generate(docs: List[Dict], name: str = "PyScGenClass", namespace: str = "com.pyscgen.avro") -> str:
    schema: str = avro_generator_service.generate_schema(
        docs=docs,
        name=name,
        namespace=namespace
    )
    return schema
