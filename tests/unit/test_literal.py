from __future__ import annotations

from typing import Literal

from pydantic import BaseModel
from pydantic2avro import PydanticToAvroSchemaMaker
from pydantic2avro.exceptions import InvalidLiteralMemeberException

import pytest
from ..utils import validate_avro_schema


def test_valid_literal_of_strings() -> None:
    class NetworkInterfaceCard(BaseModel):
        type: Literal["ethernet", "wireless", "pci"]

    
    pydantic_records = [
        NetworkInterfaceCard(type="ethernet"),
        NetworkInterfaceCard(type="wireless"),
        NetworkInterfaceCard(type="pci")
    ]

    records = [record.model_dump() for record in pydantic_records]

    schema = PydanticToAvroSchemaMaker(NetworkInterfaceCard).get_schema()

    from pprint import pprint
    pprint(schema)
    print()
    
    validate_avro_schema(schema=schema, records=records)


def test_literal_of_mix_types() -> None:
    class Cola(BaseModel):
        formula: Literal["top secret flavour", "formula #0000", 42]


    with pytest.raises(InvalidLiteralMemeberException):
        _schema = PydanticToAvroSchemaMaker(Cola).get_schema()


def test_literal_of_non_string() -> None:
    class RandomState(BaseModel):
        value: Literal[0, 1, 42]


    with pytest.raises(InvalidLiteralMemeberException):
        _schema = PydanticToAvroSchemaMaker(RandomState).get_schema()


    
