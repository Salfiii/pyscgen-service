import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.configuration.getConfig import Config
# routers
from app.routers import api_config, avro_generator, json_analyze, pydantic_generator, avro_validator, data_generator

# get the config file
from app.service.avro_generator import AvroGeneratorService

SERVICE_PORT = os.getenv("SERVICE_PORT", 8001)
GUI_PORT = os.getenv("GUI_PORT", 3000)

origins = [
    "127.0.0.1:" + str(GUI_PORT),
    "localhost:" + str(GUI_PORT),
    "http://127.0.0.1:" + str(GUI_PORT),
    "http://localhost:" + str(GUI_PORT),
    "https://127.0.0.1:" + str(GUI_PORT),
    "https://localhost:" + str(GUI_PORT),
    "http://localhost:" + str(GUI_PORT),
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://0.0.0.0",
    "https://0.0.0.0",
    "http://localhost",
    "https://localhost"
]

config = Config()

# fastAPI Instance
app = FastAPI(
    title="Pyscgen Service for AVRO Schema generation and analyzing JSON documents (API ID: "
    + str(config.API_ID) + ")", docs_url="/", version=config.API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# include the routers
app.include_router(api_config.router)
app.include_router(avro_generator.router)
app.include_router(json_analyze.router)
app.include_router(pydantic_generator.router)
app.include_router(avro_validator.router)
app.include_router(data_generator.router)

# needed to start the application locally for development/debugging purpose. Will never be called on K8s.
if config.is_local:
    import uvicorn
    if __name__ == '__main__':
        # if run locally, the port might already be in use, just use another one then.
        uvicorn.run(app, host='localhost', port=SERVICE_PORT)
