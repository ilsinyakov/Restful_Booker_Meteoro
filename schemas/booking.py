from datetime import date

from pydantic import BaseModel


class BookingDates(BaseModel):
    checkin: date
    checkout: date


class Booking(BaseModel):
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str


class BookingSchema(BaseModel):
    bookingid: int
    booking: Booking

    class Config:
        validate_by_name = True
