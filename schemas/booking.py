from datetime import date

from pydantic import BaseModel, ConfigDict


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


class CreateBookingSchema(BaseModel):
    bookingid: int
    booking: BookingSchema

    model_config = ConfigDict(validate_by_name=True)
