# pydantic2avro
Generate Apache Avro schemas from Pydantic data models. 


### Install

```bash
pip install pydantic2avro
```

### Example

* Create a file `main.py` with:
```python
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

```

* Run it
```bash
$ python main.py 
{'fields': [{'name': 'id', 'type': {'logicalType': 'uuid', 'type': 'string'}},
            {'name': 'name', 'type': 'string'},
            {'name': 'age', 'type': 'long'}],
 'name': 'User',
 'type': 'record'}
$
```

### Developing

###### Install package

- Requirement: Poetry 1.*

```shell
$ git clone https://github.com/Happy-Kunal/pydantic2avro
$ cd pydantic2avro/
$ poetry install
```

###### Run unit tests
```shell
$ pytest
$ coverage run -m pytest  # with coverage

# or (depends on your local env) 
$ poetry run pytest
$ poetry run coverage run -m pytest  # with coverage
```

### Features
- [x] Primitive types: int, long, double, float, boolean, string and null support
- [x] Complex types: enum, array, map, fixed, unions and records support
- [x] Logical Types: date, duration, time (millis and micro), datetime (millis and micro), uuid support
- [x] Recursive Schemas
- [x] Generate json from pydantic class instance



### TODO:
- [ ] write better tests.
- [ ] increase test coverage from 92% to atleast 99%.
