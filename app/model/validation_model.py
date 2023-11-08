from typing import Optional

from pydantic import BaseModel


class ValidationModel(BaseModel):
    validation_result: bool
    message: Optional[str] = None
