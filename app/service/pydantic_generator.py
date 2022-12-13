from pyscgen.pydantic.schema.create_schema import PydanticSchemaGenerator

from app.configuration.getConfig import Config


class PydanticGeneratorService:

    def __init__(self, config: Config):
        self.config = config
        self.pydantic_schema_generator: PydanticSchemaGenerator = PydanticSchemaGenerator(alphabetically_ordered_by_path=True, debug=self.config.debug)

    def generate_schema(self, docs: [dict], name: str, namespace: str) -> str:
        schema: str = self.pydantic_schema_generator.create_schema(
            docs=docs,
            name=name,
            namespace=namespace
        )
        return schema
