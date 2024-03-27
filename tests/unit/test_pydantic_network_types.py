from __future__ import annotations

from pydantic import BaseModel, EmailStr

from pydantic2avro import PydanticToAvroSchemaMaker

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


