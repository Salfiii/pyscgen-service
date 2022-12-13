from typing import Collection

from pandas import DataFrame
from pyscgen.json._model.analyze_model import ColumnInfos
from pyscgen.json.analyze.analyze_documents import JSONAnalyzer

from app.configuration.getConfig import Config


class JsonAnalyzerService:

    def __init__(self, config: Config):
        self.config = config
        self.json_analyzer: JSONAnalyzer = JSONAnalyzer()

    def analyze_json(self, docs: [dict]) -> tuple[Collection, ColumnInfos, DataFrame, DataFrame, DataFrame]:
        collection_data, column_infos, df_flattened, df_dtypes, df_unique = self.json_analyzer.analyze(
            docs=docs
        )
        return collection_data, column_infos, df_flattened, df_dtypes, df_unique
