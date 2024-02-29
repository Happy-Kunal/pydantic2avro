from pydantic import BaseModel, Field
from pydantic import model_validator

from .enums import TimePrecision


class DecimalOptions(BaseModel):
    scale: int = Field(default=0, ge=0)
    precision: int = Field(default=10, gt=0)

    @model_validator(mode="after")
    def check_scale_less_than_or_equal_to_precision(self) -> "DecimalOptions":
        if (self.scale > self.precision):
            raise ValueError("Scale must be less than or equal to the precision")
        return self



class SchemaOptions(BaseModel):
    decimal: DecimalOptions = Field(default_factory=DecimalOptions)
    time_precision: TimePrecision = TimePrecision.MILLI_SECOND
    timestamp_precision: TimePrecision = TimePrecision.MILLI_SECOND
    local_timestamp_precision: TimePrecision = TimePrecision.MILLI_SECOND
