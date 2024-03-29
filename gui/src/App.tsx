import React, { useState, useEffect } from "react";
import logo from "./GitHub-Mark-Light-120px-plus.png";
import "./App.css";
import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-json";
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-tomorrow_night";
import "ace-builds/src-noconflict/mode-yaml";

const apiUrl = "http://localhost:" + process.env.REACT_APP_SERVICE_PORT;
const defaultJsonObject = '[{\n\t"foo": 5, \n\t"barBaz": "hello", \n\t"value": "string"\n},\n{\n\t"foo": 5, \n\t"barBaz": "hello"\n}]';
const defaultNamespace = "com.pyscgen.avro"
const defaultClassName = "PyScGenClass"
const defaultOptions = { name: defaultClassName, namespace: defaultNamespace };
const loadingMessage = '{"message": "# loading..."}';
const invalidJsonMessage = '{"message": "# invalid json"}';

function App() {
  const [options, setOptions] = useState(defaultOptions);
  const [jsonObject, setJsonObject] = useState(defaultJsonObject);
  const [pydanticModel, setPydanticModel] = useState("");
  const [avroSchema, setAvroSchema] = useState("{}");
  const [dummyData, setDummyData] = useState("[]");
  const [avroValidationResult, setAvroValidationResult] = useState(false);
  const [avroValidationMessage, setAvroValidationMessage] = useState("");

  useEffect(() => {
    if (validJson(jsonObject)) {
      fetchConversion(jsonObject, "pydantic", options.name, options.namespace);
      fetchConversion(jsonObject, "avro", options.name, options.namespace);
    } else {
      setPydanticModel(invalidJsonMessage);
      setAvroSchema(invalidJsonMessage);
      setDummyData("[]")
      setAvroValidationResult(false)
      setAvroValidationMessage("")
    }
  }, [jsonObject, options]);

  function validJson(newValue: string): boolean {
    try {
      JSON.parse(newValue);
    } catch (_) {
      return false;
    }
    return true;
  }

  function onChange(newValue: string) {
    setJsonObject(newValue);
  }

  function fetchConversion(
    newValue: string,
    modelType: string,
    name: string,
    namespace: string
  ) {
    console.log("fetching schemas...");
    setPydanticModel(loadingMessage);
    const url = new URL(apiUrl + "/" + modelType + "/schema/generate?name=" + name + "&namespace=" + namespace);
    const opts = {
      method: "POST",
      headers: {
        "Content-type": "application/json"
      },
      body: newValue,
    };

    fetch(url.toString(), opts)
      .then((response) => {
        if (response.status === 422) {
          setPydanticModel(invalidJsonMessage);
        }
        return response.json();
      })
      .then((data) => {
        //console.log(data)
        if (modelType === "pydantic") {
          setPydanticModel(data);
        }
        else {
          let avro_schema = JSON.stringify(data, null, 4)
          setAvroSchema(avro_schema)
          try {
            generateDummyData(avro_schema)
          }
          catch{
            setDummyData('[{"message": "Could not generate dummy data"}]')
          }
          try {
            validateAvro(avro_schema, JSON.parse(jsonObject))
          }
          catch{
            setAvroValidationResult(false)
          }
        }
      });
  }

    function generateDummyData(
        avro_schema: string
  ) {
    console.log("generating dummy data...");
    setDummyData(loadingMessage);
    const url = new URL(apiUrl + "/avro/data/generate");
    const opts = {
      method: "POST",
      headers: {
        "Content-type": "application/json"
      },
      body: avro_schema,
    };

    fetch(url.toString(), opts)
      .then((response) => {
        if (response.status === 422) {
          setDummyData("[]");
        }
        return response.json();
      })
      .then((data) => {
        //console.log(data)
        setDummyData(JSON.stringify(data, null, 4))
      });
  }

    function validateAvro(
        avro_schema: string,
        records: [string]
  ) {
    console.log("generating dummy data...");
    setAvroValidationResult(false);
    const url = new URL(apiUrl + "/avro/schema/validate");
    const opts: RequestInit = {
      method: "POST",
      headers: {
        "Content-type": "application/json"
      },
      body: JSON.stringify({
        "avro_schema": JSON.parse(avro_schema),
        "records": records
      })
    };
    fetch(url.toString(), opts)
      .then((response) => {
        if (response.status === 422) {
          setAvroValidationResult(false);
        }
        return response.json();
      })
      .then((data) => {
        //console.log(data)
        setAvroValidationResult(data.validation_result===true)
        setAvroValidationMessage(data.message)
      });
  }

  return (
    <div className="App">
      <h1>PyScGen (Python Schema Generator) Service</h1>
      <h2> <a href="https://github.com/Salfiii/pyscgen">
            Backend Docs (pyscgen)
          </a></h2>
      <div className="editor-container">
        <div className="editor">
          <h3>JSON</h3>
          <AceEditor
            value={jsonObject}
            mode="json"
            theme="tomorrow_night"
            onChange={onChange}
            name="json-editor"
            editorProps={{ $blockScrolling: true }}
          />
        </div>
        <div className="editor">
          <h3>Pydantic</h3>
          <AceEditor
            value={pydanticModel}
            mode="python"
            theme="tomorrow_night"
            name="python-editor"
            editorProps={{ $blockScrolling: true }}
          />
        </div>
        <div className="editor">
          <h3>AVRO</h3>
          <AceEditor
            value={avroSchema}
            mode="yaml"
            theme="tomorrow_night"
            name="avro-editor"
            editorProps={{ $blockScrolling: true }}
          />
          <p></p>
          <div>Valid: {avroValidationResult.toString()}</div>
          <p></p>
          <div>Message: {avroValidationMessage}</div>
        </div>
        <div className="editor">
          <h3>DUMMY DATA</h3>
          <AceEditor
            value={dummyData}
            mode="json"
            theme="tomorrow_night"
            name="dummy-data-editor"
            editorProps={{ $blockScrolling: true }}
          />
          <p></p>
          <button onClick={() => generateDummyData(avroSchema)} >Refresh</button>
        </div>
      </div>
      <div className="options-container">
        <h3>Options</h3>
        <div className="option">
          <p className="control">
            <label className="checkbox">
              <input
                  className="option-text"
                  defaultValue={defaultClassName}
                type="text"
                onChange={(e) =>
                  setOptions({ ...options, name: e.target.value })
                }
              />
              Class name
            </label>
          </p>
        </div>
        <div className="field">
          <p className="option">
            <label className="checkbox">
              <input
                  className="option-text"
                  defaultValue={defaultNamespace}
                type="text"
                onChange={(e) =>
                  setOptions({ ...options, namespace: e.target.value })
                }
              />
              Namespace
            </label>
          </p>
        </div>
      </div>
      <br></br>
      <div className="about">
        <h2>What is this?</h2>
        <p>
          PyScgen (Python Schema Generator) is a tool that lets you convert JSON objects into
          AVRO Schemas and Pydantic models.
          <li>
          <a href="https://www.json.org/json-en.html">JSON</a>{" "}
          is the de-facto data interchange format of the internet, and{" "}
          </li>
          <li>
          <a href="https://pydantic-docs.helpmanual.io/">Pydantic</a> is a
          library that makes parsing JSON in Python a breeze.
          </li>
          <li>
          <a href="https://avro.apache.org/docs/">Apache Avro™</a>  is a data serialization system and quite often used together with Kafka.
          </li>

        </p>
        <p>
          To generate schemas from a JSON objects, enter them as an array into the
          JSON editor and watch the schemas automagically appear in the
          editors.
        </p>
        <p>
          Models are generated via {" "}
          <a href="https://github.com/Salfiii/pyscgen">
            pyscgen Python package
          </a>
          .
        </p>
      </div>
      <a href="https://github.com/Salfiii/pyscgen-service">
        <img id="github-logo" src={logo} alt="GitHub Logo" />
      </a>
    </div>
  );
}

export default App;
