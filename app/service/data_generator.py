from typing import Dict, List

from fastavro.utils import generate_many


from app.configuration.getConfig import Config


class DataGeneratorService:

    def __init__(self, config: Config):
        self.config = config

    def generate(self, avro_schema: str, number_of_recors: int = 5) -> List[Dict]:
        dummy_data = generate_many(schema=avro_schema, count=number_of_recors)
        return [data for data in dummy_data]
    