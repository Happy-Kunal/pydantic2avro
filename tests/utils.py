import json
from io import BytesIO

import fastavro


def validate_avro_schema(schema: str | dict, records: list) -> None:
    records = records.copy()
    if isinstance(schema, str):
        schema = json.loads(schema)

    # schema = fastavro.parse_schema(schema)
    #schema = fastavro.parse_schema(schema)
    from fastavro import _schema_py
    schema = _schema_py.parse_schema(schema=schema)

    fobj = BytesIO()
    fastavro.writer(fobj, schema=schema, records=records)

    fobj.seek(0)
    print(fobj.read())
    fobj.seek(0)

    print("writing successful")

    for record in fastavro.reader(fobj):
        if (record not in records):
            print(f"{record} not present in {records}")
            raise ValueError(f"{record} not present in {records}")
        else:
            records.remove(record)
    
    print("reading successful")
