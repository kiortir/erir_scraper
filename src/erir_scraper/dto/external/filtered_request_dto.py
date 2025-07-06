from typing import Literal
from pydantic import BaseModel


class FilterRequestBody(BaseModel):
    page: int
    size: int = 10
    sortField: str = "createdDate"
    sortOrder: Literal["asc", "desc"] = "desc"
