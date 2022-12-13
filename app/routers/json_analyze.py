import json
from typing import Dict, List, _SpecialForm

from fastapi import  APIRouter
from pyscgen.json._model.analyze_model import ColumnInfos

from app.configuration.getConfig import Config
from app.service.json_analyzer import JsonAnalyzerService


config = Config()
json_analyzer_service: JsonAnalyzerService = JsonAnalyzerService(config=config)

# fastAPI Instance
router = APIRouter()

# Logger
logger = config.logger


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, type):
            return str(obj)
        elif isinstance(obj, _SpecialForm):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


@router.post("/json/analyze", tags=["json"])
async def json_analyze(docs: List[Dict]):
    collection_data, column_info, _, _, _ = json_analyzer_service.analyze_json(
        docs=docs
    )
    column_info_dict = json.loads(json.dumps(column_info.as_dict(), cls=ComplexEncoder, indent=4))
    return column_info_dict
