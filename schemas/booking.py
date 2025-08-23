from datetime import date

from pydantic import BaseModel


class BookingDates(BaseModel):
    checkin: date
    checkout: date


class BookingSchema(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str

    class Config:
        allow_population_by_field_name = True
