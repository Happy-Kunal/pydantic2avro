from __future__ import annotations

from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from pydantic2avro import PydanticToAvroSchemaMaker
from pydantic2avro import SchemaOptions, DecimalOptions

from .utils import validate_avro_schema


class DiscountOffers(str, Enum):
    TEN_PERCENT_OFF = "TEN_PERCENT_OFF"
    TWENTY_PERCENT_OFF = "TWENTY_PERCENT_OFF"
    TWENTY_FIVE_PERCENT_OFF = "TWENTY_FIVE_PERCENT_OFF"
    FIFTY_PERCENT_OFF = "FIFTY_PERCENT_OFF"
    SEVENTY_FIVE_PERCENT_OFF = "SEVENTY_FIVE_PERCENT_OFF"
    NINETY_PERCENT_OFF = "NINETY_PERCENT_OFF"

class FreeProductOffer(str, Enum):
    FREE_SAMPLE = "FREE_SAMPLE"
    BUY_ONE_GET_ONE_FREE = "BUY_ONE_GET_ONE_FREE"
    BUY_TWO_GET_ONE_FREE = "BUY_TWO_GET_ONE_FREE"

class Manufacturer(BaseModel):
    name: str
    country: str


class Product(BaseModel):
    pid: UUID
    tags: list[str] | None
    offers: list[DiscountOffers | FreeProductOffer] | None
    similar_products: list[UUID] | None
    complementary_products: list[Product] | None
    details: dict[str, None | int | str | dict[str, str | list[str]] | Manufacturer] | None


def test_complex_types() -> None:
    products = [
        Product(
            pid=uuid4(),
            tags=["electronics", "longer battery life", "value for money"],
            offers=[FreeProductOffer.BUY_TWO_GET_ONE_FREE],
            similar_products=[uuid4(), uuid4(), uuid4(), uuid4()],
            complementary_products=None,
            details={
                "mfg. year": 2024,
                "manufacturer": Manufacturer(
                    name="SomeGoodManufacturer",
                    country="India"
                ),
                "specs": {
                    "body": "titanium",
                    "battery": "5000mAh",
                    "connectivity": [
                        "cellular", 
                        "wifi",
                        "bluetooth"
                    ]
                }
            }
        )
    ]

    records = [product.model_dump() for product in products]

    schema = PydanticToAvroSchemaMaker(schema_name="Product", namespace="sharma.kunal", pydantic_model=Product).get_schema()

    from pprint import pprint
    pprint(schema)
    print()
    
    validate_avro_schema(schema=schema, records=records)


