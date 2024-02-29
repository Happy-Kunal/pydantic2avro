from enum import Enum, auto

class AvroDataTypes(str, Enum):
    NULL = "null"
    BOOLEAN = "boolean"
    INT = "int"
    LONG = "long"
    FLOAT = "float"
    DOUBLE = "double"
    BYTES = "bytes"
    STRING = "string"
    ENUM = "enum"
    ARRAY = "array"
    MAP = "map"
    FIXED = "fixed"
    RECORD = "record"

class AvroLogicalTypes(str, Enum):
    DECIMAL = "decimal"
    UUID = "uuid"
    DATE = "date"
    TIME_MILLIS = "time-millis"
    TIME_MICROS = "time-micros"
    TIMESTAMP_MILLIS = "timestamp-millis"
    TIMESTAMP_MICROS = "timestamp-micros"
    LOCAL_TIMESTAMP_MILLIS = "timestamp-millis"
    LOCAL_TIMESTAMP_MICROS = "timestamp-micros"
    DURATION = "duration"


MAP_AVRO_LOGICAL_TYPE_TO_AVRO_DATA_TYPE = {
    AvroLogicalTypes.DECIMAL: AvroDataTypes.BYTES,
    AvroLogicalTypes.UUID: AvroDataTypes.STRING,
    AvroLogicalTypes.DATE: AvroDataTypes.INT,
    AvroLogicalTypes.TIME_MILLIS: AvroDataTypes.INT,
    AvroLogicalTypes.TIME_MICROS: AvroDataTypes.LONG,
    AvroLogicalTypes.TIMESTAMP_MILLIS: AvroDataTypes.LONG,
    AvroLogicalTypes.TIMESTAMP_MICROS: AvroDataTypes.LONG,
    AvroLogicalTypes.LOCAL_TIMESTAMP_MILLIS: AvroDataTypes.LONG,
    AvroLogicalTypes.LOCAL_TIMESTAMP_MICROS: AvroDataTypes.LONG,
    AvroLogicalTypes.DURATION: AvroDataTypes.FIXED
}


class TimePrecision(Enum):
    MILLI_SECOND = auto()
    MICRO_SECOND = auto()
