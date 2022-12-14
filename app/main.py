
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.configuration.getConfig import Config
# routers
from app.routers import api_config, avro_generator, json_analyze, pydantic_generator

# get the config file
from app.service.avro_generator import AvroGeneratorService

PORT = 8001

origins = [
    "127.0.0.1:" + str(PORT),
    "localhost:" + str(PORT),
    "http://127.0.0.1:" + str(PORT),
    "http://localhost:" + str(PORT),
    "http://localhost:3000",
    "localhost:3000"
]

config = Config()

# fastAPI Instance
app = FastAPI(
    title="Pyscgen Service for AVRO Schema generation and analyzing JSON documents (API ID: "
    + str(config.API_ID) + ")", docs_url="/", version=config.API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# include the routers
app.include_router(api_config.router)
app.include_router(avro_generator.router)
app.include_router(json_analyze.router)
app.include_router(pydantic_generator.router)

# needed to start the application locally for development/debugging purpose. Will never be called on K8s.
if config.is_local:
    import uvicorn
    if __name__ == '__main__':
        # if run locally, the port might already be in use, just use another one then.
        uvicorn.run(app, host='127.0.0.1', port=PORT)
