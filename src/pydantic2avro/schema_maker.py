import builtins
import datetime
import decimal
import inspect
import json
import types
import typing
import uuid
from enum import Enum
from functools import partial
from typing import Type, get_args, get_origin

import pydantic
from pydantic import BaseModel
import pydantic.networks

from .enums import (MAP_AVRO_LOGICAL_TYPE_TO_AVRO_DATA_TYPE, AvroDataTypes,
                    AvroLogicalTypes, TimePrecision)
from .exceptions import (InvalidEnumMemeberException,
                         InvalidLiteralMemeberException,
                         NotAnAvroLogicalDataTypeException,
                         NotAnAvroPrimitiveDataTypeException,
                         NotAPydanticModelException, UnsupportedTypeException)
from .schema_component_types import AvroSchemaComponent
from .schema_options import SchemaOptions


def get_avro_equivalent_type_for(
    type_: type,
    namespace: str | None,
    fieldname: str | None,
    schema_options: SchemaOptions,
    dp: dict[Type[Enum] | Type[BaseModel], str],
) -> str | AvroSchemaComponent:
    if AvroTypeExpert.has_avro_primitive_type_equivalent_for(type_):
        return AvroTypeExpert.get_avro_primitive_type_equivalent_for(type_).value
    
    elif AvroTypeExpert.has_avro_logical_type_equivalent_for(type_):
        return AvroTypeExpert.get_avro_logical_type_equivalent_for(
            type_,
            schema_options=schema_options
        )
    
    elif AvroTypeExpert.type_in_pydantic_networks_field(type_):
        return AvroTypeExpert.get_avro_equivaluent_for_pydantic_networks_field(type_)
    
    else:
        return AvroTypeExpert.get_avro_complex_type_equivalent_for(
            type_,
            namespace=namespace,
            fieldname=fieldname,
            schema_options=schema_options,
            dp=dp
        )


class AvroTypeExpert:
    @staticmethod
    def has_avro_primitive_type_equivalent_for(type_: type) -> bool:
        return type_ in (types.NoneType, bool, int, float, bytes, str)

    @staticmethod
    def has_avro_logical_type_equivalent_for(type_: type) -> bool:
        return type_ in (
            decimal.Decimal,
            uuid.UUID,
            datetime.date,
            datetime.time,
            datetime.datetime,
            datetime.timedelta,
            pydantic.AwareDatetime,
            pydantic.NaiveDatetime,
        )
    

    @staticmethod
    def type_in_pydantic_networks_field(type_: type):
        return (
            type(type_) is not types.UnionType
            and type_.__name__ in pydantic.networks.__all__
        )

    @staticmethod
    def get_avro_primitive_type_equivalent_for(type_: type) -> AvroDataTypes:
        match type_:
            case types.NoneType:
                return AvroDataTypes.NULL
            case builtins.bool:
                return AvroDataTypes.BOOLEAN
            case builtins.int:
                return AvroDataTypes.LONG  # intentional
            case builtins.float:
                return AvroDataTypes.DOUBLE  # intentional
            case builtins.bytes | builtins.bytearray:
                return AvroDataTypes.BYTES
            case builtins.str:
                return AvroDataTypes.STRING
            case _:
                raise NotAnAvroPrimitiveDataTypeException
            

    @staticmethod
    def get_avro_logical_type_equivalent_for(
        type_: type, schema_options: SchemaOptions
    ) -> AvroSchemaComponent:

        other_fields: dict[str, str | int] = dict()

        match type_:
            case decimal.Decimal:
                logical_type = AvroLogicalTypes.DECIMAL
                other_fields.update(
                    precision=schema_options.decimal.precision,
                    scale=schema_options.decimal.scale,
                )

            case uuid.UUID:
                logical_type = AvroLogicalTypes.UUID

            case datetime.timedelta:
                logical_type = AvroLogicalTypes.DURATION
                other_fields.update(size=12)

            case datetime.date:
                logical_type = AvroLogicalTypes.DATE

            case datetime.time:
                if schema_options.time_precision is TimePrecision.MILLI_SECOND:
                    logical_type = AvroLogicalTypes.TIME_MILLIS
                else:
                    logical_type = AvroLogicalTypes.TIME_MICROS

            case datetime.datetime | pydantic.NaiveDatetime:
                if schema_options.timestamp_precision is TimePrecision.MILLI_SECOND:
                    logical_type = AvroLogicalTypes.TIMESTAMP_MILLIS
                else:
                    logical_type = AvroLogicalTypes.TIMESTAMP_MICROS

            case pydantic.AwareDatetime:
                if (
                    schema_options.local_timestamp_precision
                    is TimePrecision.MILLI_SECOND
                ):
                    logical_type = AvroLogicalTypes.LOCAL_TIMESTAMP_MILLIS
                else:
                    logical_type = AvroLogicalTypes.LOCAL_TIMESTAMP_MICROS

            case _:
                raise NotAnAvroLogicalDataTypeException

        return dict(
            type=MAP_AVRO_LOGICAL_TYPE_TO_AVRO_DATA_TYPE[logical_type].value,
            logicalType=logical_type.value,
            **other_fields,
        )
    
    @staticmethod
    def get_avro_equivaluent_for_pydantic_networks_field(type_: type):
        return dict(
            type=AvroDataTypes.STRING,
            __pydantic_class=type_.__name__
        )

    @staticmethod
    def get_avro_complex_type_equivalent_for(
        type_: type,
        namespace: str | None,
        fieldname: str | None,
        schema_options: SchemaOptions,
        dp: dict[Type[Enum] | Type[BaseModel], str],
    ) -> AvroSchemaComponent:

        if type_ in dp:
            return dp[type_]
        elif inspect.isclass(type_):
            dp[type_] = f"{namespace}.{type_.__name__}" if namespace else type_.__name__

            if issubclass(type_, Enum):
                for enum_member in iter(type_):
                    if not isinstance(enum_member.value, str):  # TODO: add regex check
                        raise InvalidEnumMemeberException(
                            f"Avro only allow strings to be value of Enums'"
                            f" members' value. ({type_} does not follow this)"
                        )

                return dict(
                    name=dp[type_],
                    type=AvroDataTypes.ENUM.value,
                    symbols=[member.value for member in iter(type_)],
                )

            elif issubclass(type_, BaseModel):
                return PydanticToAvroSchemaMaker(
                    schema_name=dp[type_],
                    namespace=namespace,
                    pydantic_model=type_,
                    schema_options=schema_options,
                    dp=dp,
                ).get_schema()

        partial_get_avro_equivalent_type_for = partial(
            get_avro_equivalent_type_for,
            namespace=namespace,
            fieldname=fieldname,
            schema_options=schema_options,
            dp=dp,
        )

        match get_origin(type_):
            case builtins.list:
                elements_type = get_args(type_)[0]
                return dict(
                    type=AvroDataTypes.ARRAY.value,
                    items=partial_get_avro_equivalent_type_for(elements_type),
                )

            case builtins.dict:
                key_type, value_type = get_args(type_)
                if key_type is not str:
                    raise UnsupportedTypeException("dict keys must be str")

                return dict(
                    type=AvroDataTypes.MAP.value,
                    values=partial_get_avro_equivalent_type_for(value_type),
                )

            case types.UnionType:
                union_schema = list()
                for member_type in get_args(type_):
                    union_schema.append(
                        partial_get_avro_equivalent_type_for(member_type)
                    )

                return union_schema
            
            case typing.Literal:
                for literal_member in get_args(type_):
                    if not isinstance(literal_member, str):  # TODO: add regex check
                        raise InvalidLiteralMemeberException(
                            f"In pydantic2avro python's `Literal` are "
                            f"coerced to Enums. since, "
                            f"Avro only allow strings to be value of Enums' "
                            f"members' value. ({type_} does not follow this)"
                        )

                return dict(
                    name=f"{namespace}.{fieldname}" if namespace else fieldname,
                    type=AvroDataTypes.ENUM.value,
                    symbols=[member for member in get_args(type_)],
                )

            case _:
                raise UnsupportedTypeException(f"{type_} is unsupported")
                        


class PydanticToAvroSchemaMaker:
    def __init__(
        self,
        pydantic_model: Type[BaseModel],
        *,
        namespace: str | None = None,
        schema_name: str | None = None,
        schema_options: SchemaOptions = SchemaOptions(),
        dp: dict[Type[Enum] | Type[BaseModel], str] | None = None,
    ) -> None:

        if not issubclass(pydantic_model, BaseModel):
            raise NotAPydanticModelException

        schema_name = schema_name or pydantic_model.__name__

        self.pydantic_model = pydantic_model
        self.namespace = namespace
        self.schema_name = (
            f"{namespace}.{schema_name}"
            if (schema_name.count(".") == 0 and namespace is not None)
            else schema_name
        )
        self.schema_options = schema_options
        self._schema = dict(name=self.schema_name, type="record", fields=list())
        self.dp: dict[Type[Enum] | Type[BaseModel], str] = dp or dict()

        self.dp.update({self.pydantic_model: self.schema_name})

        self.__construct_schema()

    def __construct_schema(self):

        for fieldname, fieldinfo in self.pydantic_model.model_fields.items():
            curr = dict(name=fieldname)
            fieldtype = fieldinfo.annotation

            if fieldtype in self.dp:
                curr.update(type=self.dp.get(fieldtype))
            else:
                curr.update(
                    type=get_avro_equivalent_type_for(
                        fieldtype,
                        namespace=self.namespace,
                        fieldname=fieldname,
                        schema_options=self.schema_options,
                        dp=self.dp,
                    )
                )

            self._schema["fields"].append(curr)

    def get_schema(self):
        return self._schema.copy()

    def get_schema_str(self):
        return json.dumps(self._schema)
