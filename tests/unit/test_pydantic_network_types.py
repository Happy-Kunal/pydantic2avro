from __future__ import annotations

from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr

from pydantic2avro import PydanticToAvroSchemaMaker
from pydantic2avro import SchemaOptions, DecimalOptions

from ..utils import validate_avro_schema




def test_email() -> None:
    class EmailModel(BaseModel):
        email: EmailStr

    pydantic_records = [
        EmailModel(email="hello.world@example.com"),
        EmailModel(email="foo+bar@baz.com"),
        EmailModel(email="foo_bar@hello.world.com")
    ]

    records = [record.model_dump() for record in pydantic_records]

    schema = PydanticToAvroSchemaMaker(EmailModel).get_schema()

    from pprint import pprint
    pprint(schema)
    print()
    
    validate_avro_schema(schema=schema, records=records)


