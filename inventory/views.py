from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Member, Inventory, Booking

MAX_BOOKINGS = 2

def book_item(request, member_id, inventory_id):
    try:
        member = get_object_or_404(Member, id=member_id)
        inventory = get_object_or_404(Inventory, id=inventory_id)

        # Check booking limits
        if Booking.objects.filter(member=member).count() >= MAX_BOOKINGS:
            return JsonResponse({'error': 'Max booking limit reached'}, status=400)

        if inventory.remaining_count <= 0:
            return JsonResponse({'error': 'Item out of stock'}, status=400)

        # Create booking
        booking = Booking.objects.create(member=member, inventory=inventory, booking_date=now())

        # Update inventory
        inventory.remaining_count -= 1
        inventory.save()

        return JsonResponse({'message': 'Booking successful', 'booking_id': booking.id})
    except Exception as e:
        return JsonResponse({'Error':str(e)})

def cancel_booking(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Restore inventory count
        booking.inventory.remaining_count += 1
        booking.inventory.save()

        # Delete booking
        booking.delete()

        return JsonResponse({'message': 'Booking cancelled successfully'})
    except Exception as e:
        return JsonResponse({'Error':str(e)})
