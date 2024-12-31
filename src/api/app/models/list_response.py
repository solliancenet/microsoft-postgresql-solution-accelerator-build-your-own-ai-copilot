from pydantic import BaseModel
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class ListResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    skip: int
    limit: int
