from django.urls import path
from django.conf.urls import handler404, handler500
from .views import book_item, cancel_booking
from booking_system.exception_handlers import custom_404_handler, custom_500_handler

handler404 = custom_404_handler
handler500 = custom_500_handler
urlpatterns = [
    path('book/<int:member_id>/<int:inventory_id>/', book_item, name='book_item'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]
