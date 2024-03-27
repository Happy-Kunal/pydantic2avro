class NotAPydanticModelException(Exception):
    pass

class NotAnAvroPrimitiveDataTypeException(Exception):
    pass

class NotAnAvroLogicalDataTypeException(Exception):
    pass

class UnsupportedTypeException(Exception):
    pass

class InvalidEnumMemeberException(Exception):
    pass

class InvalidLiteralMemeberException(Exception):
    pass
