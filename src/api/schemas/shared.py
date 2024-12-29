from pydantic import BaseModel
from typing import List, Optional, TypeVar, Generic
from pydantic.generics import GenericModel

T = TypeVar('T')

class ListResponse(GenericModel, Generic[T]):
    data: List[T]
    total: int
    skip: int
    limit: int
