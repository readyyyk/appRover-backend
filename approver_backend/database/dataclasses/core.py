from pydantic import BaseModel as PydanticBase, ConfigDict
from pydantic.functional_validators import WrapValidator, AfterValidator, PlainValidator
from typing import Annotated, TYPE_CHECKING


class BaseModel(PydanticBase):
    model_config = ConfigDict(
        from_attributes=True
    )


__all__ = [
    'BaseModel',
    'WrapValidator',
    'AfterValidator',
    'PlainValidator',
    'Annotated',
    'TYPE_CHECKING'
]
