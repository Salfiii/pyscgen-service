# Pyscgen-service
A single page web app to create [AVRO](https://avro.apache.org/docs/1.11.1/) & [Pydantic](https://docs.pydantic.dev/) Schemas based on multiple JSON documents/strings.
Just paste some JSON Strings as an array and watch the Schemas appear. 

The cool part is, that it also handles nullability based on the data provided and missing fields in the documents. To infer nullability, at leas two documents are needed.

The Schema creation is realized with the Python Package [pyscgen](https://github.com/Salfiii/pyscgen)

**PLEASE NOTE**: 
- The app is currently work in progress but is running fine on my end.
- I´d love to publicly host a version as a showcase but sadly heroku canceled the free plan and I´m currently looking for cheap solution to do so.
- I´m planing to publish a version to Dockerhub for a more convenient access and installation routine.

![screenshot.PNG](misc%2Fscreenshot.PNG)

## Technologies used:
- [Poetry](https://python-poetry.org/)
- [FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI & Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Docker](https://www.docker.com/101-tutorial)
- [React](https://reactjs.org/)
- [Node.js](https://nodejs.org/)
- [Typescript](https://www.typescriptlang.org/)
- [nginx](https://www.nginx.com/)

## How to run the app locally

## Docker

1. Clone the template
    - ``git clone https://github.com/Salfiii/pyscgen-service.git``
2. (install [poetry](https://python-poetry.org/docs/) if you want to run it locally)
3. Install [Docker](https://www.docker.com/products/docker-desktop/) or use a remote machine if you have one
4. Run the dockerfile (you can change "pyscgen-service" to whatever you like):
   - ``docker build -t pyscgen-service . && docker run -it -p 50001:80 pyscgen-service``
   - If you want to remove the dockerfile after exiting the service automatically, add "--rm" before "-it"
   - You can change the port 50001 to whatever port you want to use on your host
5. Open http://localhost:50001 in your browser and you should see the OpenAPI docs.

## With and IDE
You need to have Python 3.10 (or newer), node.js + npm and poetry installed, so Docker is way easier.

1. run the [main.py](app/main.py) to start the Python webservice
2. change directory to the gui folder in your CMD/shell and run the command
   - ``cd gui`` 
   - ``npm start``
3. Open http://localhost:3000 in your browser and you should see the GUI. to access the OpenAPI docs, use Port 8001.

