# pydantic2avro
Generate Apache Avro schemas for Pydantic data models. 


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
