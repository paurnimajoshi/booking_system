from django.urls import path
from .views import book_item, cancel_booking

urlpatterns = [
    path('book/<int:member_id>/<int:inventory_id>/', book_item, name='book_item'),
    path('cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
]
