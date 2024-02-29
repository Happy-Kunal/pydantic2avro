from pprint import pprint
from uuid import UUID

from pydantic import BaseModel
from pydantic2avro import PydanticToAvroSchemaMaker


class User(BaseModel):
    id: UUID
    name: str
    age: int

schema = PydanticToAvroSchemaMaker(User).get_schema()
pprint(schema)
