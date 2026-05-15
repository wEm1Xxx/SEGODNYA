from Models.BookingServices import BookingServices

class BookingServicesController:
    @classmethod
    def get(cls):
        return BookingServices.select()

    @classmethod
    def get_by_booking(cls, booking_id):
        return BookingServices.select().where(BookingServices.booking_id == booking_id)

    @classmethod
    def show(cls, id):
        return BookingServices.get_or_none(BookingServices.id == id)

    @classmethod
    def add_service(cls, booking_id, service_id, quantity, price_at_booking):
        return BookingServices.create(
            booking_id=booking_id,
            service_id=service_id,
            quantity=quantity,
            price_at_booking=price_at_booking
        )

    @classmethod
    def remove_service(cls, id):
        BookingServices.delete().where(BookingServices.id == id).execute()