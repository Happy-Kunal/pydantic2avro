from enum import Enum
from uuid import UUID, uuid4
from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from pydantic2avro import PydanticToAvroSchemaMaker
from pydantic2avro import SchemaOptions, DecimalOptions

from .utils import validate_avro_schema


class GenderType(str, Enum):
        MALE   = "MALE"
        FEMALE = "FEMALE"
        OTHERS = "OTHERS"

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: int
    country: str

class BankAccount(BaseModel):
    account_number: int = Field(ge=1e10, le=1e16)
    account_holder_name: str
    balance: Decimal



def test_ptasm_simple() -> None:
    class SimpleHotelBill(BaseModel):
        customer_name: str
        ordered_cnt: int
        amount: float
        paid: bool


    records = [
        SimpleHotelBill(
            customer_name="hello",
            ordered_cnt=2,
            amount=101.00,
            paid=True
        ),
        SimpleHotelBill(
            customer_name="hero hira lal",
            ordered_cnt=1,
            amount=51,
            paid=False
        )
    ]

    schema = PydanticToAvroSchemaMaker(schema_name="simple_hotel_bill", namespace="sharma.kunal", pydantic_model=SimpleHotelBill).get_schema()
    
    from pprint import pprint
    pprint(schema)
    print()
    
    records = [record.model_dump() for record in records]

    validate_avro_schema(schema=schema, records=records)


def test_ptasm_nested_with_enum() -> None:

    class Person(BaseModel):
        pid: UUID
        name: str
        address: Address
        dob: date
        gender: GenderType
        bank_acc: BankAccount
        
    persons = [
        Person(
            pid=uuid4(),
            name="Foo Bar",
            address=Address(
                street="XXXX Siebarth Dr",
                city="Lake Charles",
                state="Louisiana",
                zip_code=70615,
                country="United States"
            ),
            dob=date(year=1970, month=1, day=1),
            gender=GenderType.MALE,
            bank_acc=BankAccount(
                account_number=123456789010,
                account_holder_name="Mr. Foo Bar",
                balance=Decimal("1001001.51")
            )
        ),
        Person(
            pid=uuid4(),
            name="Bar Buzz",
            address=Address(
                street="XXXX Jammes Rd",
                city="Jacksonville",
                state="Florida",
                zip_code=32210,
                country="United States"
            ),
            dob=date(year=1970, month=12, day=31),
            gender=GenderType.FEMALE,
            bank_acc=BankAccount(
                account_number=109876543210,
                account_holder_name="Dr. Buzz",
                balance=Decimal("501701.21")
            )
        ),
    ]

    records = [person.model_dump() for person in persons]

    schema_options = SchemaOptions(decimal=DecimalOptions(scale=2, precision=10))
    schema = PydanticToAvroSchemaMaker(schema_name="person", namespace="sharma.kunal", pydantic_model=Person, schema_options=schema_options).get_schema()
    
    validate_avro_schema(schema=schema, records=records)


def test_ptasm_nested_lvl_3_with_enum() -> None:
    class ExtendedBankAccount(BankAccount):
        bank_name: str
        branch: str
        bank_address: Address

    class Person(BaseModel):
        pid: UUID
        name: str
        present_address: Address
        permanent_address: Address
        dob: date
        gender: GenderType
        bank_acc: ExtendedBankAccount

    
    persons = [
        Person(
            pid=uuid4(),
            name="Foo Bar",
            present_address=Address(
                street="XXXX Siebarth Dr",
                city="Lake Charles",
                state="Louisiana",
                zip_code=70615,
                country="United States"
            ),
            permanent_address=Address(
                street="XXXX Siebarth Dr",
                city="Lake Charles",
                state="Louisiana",
                zip_code=70615,
                country="United States"
            ),
            dob=date(year=1970, month=1, day=1),
            gender=GenderType.MALE,
            bank_acc=ExtendedBankAccount(
                account_number=123456789010,
                account_holder_name="Mr. Foo Bar",
                balance=Decimal("1001001.51"),
                bank_name="Example Bank",
                branch="The Good Branch",
                bank_address=Address(
                    street="XXXX W 32nd Ave",
                    city="Denver",
                    state="Colorado",
                    country="United States",
                    zip_code=80211
                )
            )
        ),
        Person(
            pid=uuid4(),
            name="Bar Buzz",
            present_address=Address(
                street="XXXX Jammes Rd",
                city="Jacksonville",
                state="Florida",
                zip_code=32210,
                country="United States"
            ),
            permanent_address=Address(
                street="XXX XXth Ave NE",
                city="Waseca",
                state="Minnesota",
                zip_code=56093,
                country="United States"
            ),
            dob=date(year=1970, month=12, day=31),
            gender=GenderType.FEMALE,
            bank_acc=ExtendedBankAccount(
                account_number=109876543210,
                account_holder_name="Dr. Buzz",
                balance=Decimal("501701.21"),
                bank_name="Example Bank",
                branch="The Good Branch",
                bank_address=Address(
                    street="XXXX W 32nd Ave",
                    city="Denver",
                    state="Colorado",
                    country="United States",
                    zip_code=80211
                )
            )
        ),
    ]

    records = [person.model_dump() for person in persons]

    schema_options = SchemaOptions(decimal=DecimalOptions(scale=2, precision=10))
    schema = PydanticToAvroSchemaMaker(schema_name="person", namespace="sharma.kunal", pydantic_model=Person, schema_options=schema_options).get_schema()


    from pprint import pprint
    pprint(schema)
    print()
    
    validate_avro_schema(schema=schema, records=records)






