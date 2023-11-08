from typing import List, Any

import fastavro
from fastavro._validate_common import ValidationError

from app.configuration.getConfig import Config


class AvroValidatorService:

    def __init__(self, config: Config):
        self.config = config

    def validate(self, avro_schema: dict, records: List[dict]) -> (bool, str):
        """

        """
        result: bool = False
        message: str = "The schema is valid"
        try:
            result = fastavro.validation.validate_many(schema=avro_schema, records=records, raise_errors=True)
        except ValidationError as e:
            print(e)
            message = e.__str__().split(",")[-1].replace("\n", "")[:-1]
        return result, message
