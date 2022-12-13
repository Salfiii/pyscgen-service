from pyscgen.avro._model.record_model import Schema
from pyscgen.avro.schema.create_schema import AvroSchemaGenerator

from app.configuration.getConfig import Config


class AvroGeneratorService:

    def __init__(self, config: Config):
        self.config = config
        self.avro_schema_generator: AvroSchemaGenerator = AvroSchemaGenerator(alphabetically_ordered_by_path=True, debug=self.config.debug)

    def generate_schema(self, docs: [dict], name: str, namespace: str) -> Schema:
        schema: Schema = self.avro_schema_generator.create_schema(
            docs=docs,
            name=name,
            namespace=namespace
        )
        return schema
