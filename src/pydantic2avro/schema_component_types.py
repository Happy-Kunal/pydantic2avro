from typing import Union

AvroSchemaComponent = Union[
    str,
    list["AvroSchemaComponent"],
    dict[str, Union[int, "AvroSchemaComponent"]]
]
