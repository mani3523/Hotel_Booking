from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import BookingForm
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import razorpay

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))


# Create your views
def home(request):
    hotels = Hotel.objects.all()[:3]  # Show only 6 hotels on the home page
    return render(request, 'home.html', {'hotels': hotels})
# List all hotels
@login_required(login_url='login')
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})

# Show details of a single hotel and its available rooms
@login_required(login_url='login')
def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, is_available=True)  # Fetch rooms only for this hotel
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'rooms': rooms})

@login_required(login_url='login')
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Ensure only the selected hotel's rooms are shown
    hotel_rooms = Room.objects.filter(hotel=room.hotel, is_available=True)

    if room not in hotel_rooms:
        messages.error(request, "Invalid room selection.")
        return redirect('hotel_detail', hotel_id=room.hotel.id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room  # Assign the room manually

            # Ensure room availability for the selected dates
            existing_bookings = Booking.objects.filter(
                room=room,
                check_in__lt=booking.check_out,
                check_out__gt=booking.check_in
            )

            if existing_bookings.exists():
                messages.error(request, "Room is not available for the selected dates.")
                return redirect('book_room', room_id=room.id)

            booking.save()
            return redirect(reverse('initiate_payment', args=[booking.id]))

    else:
        form = BookingForm()

    return render(request, 'hotels/book_room.html', {'form': form, 'room': room})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})


@login_required
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if not booking.total_price or booking.total_price <= 0:
        messages.error(request, "Invalid booking amount. Please try again.")
        return redirect('my_bookings')

    amount = int(booking.total_price * 100)  # Convert to paise

    # Create order in Razorpay
    razorpay_order = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    # Save order details
    payment = Payment.objects.create(
        user=request.user,
        booking=booking,
        razorpay_order_id=razorpay_order['id'],
        amount=booking.total_price
    )

    return render(request, "hotels/initiate_payment.html", {
        "razorpay_key": settings.RAZORPAY_API_KEY,
        "razorpay_order_id": razorpay_order['id'],
        "amount": booking.total_price,
        "booking": booking
    })
    
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = request.POST
        payment_id = data.get("razorpay_payment_id")
        order_id = data.get("razorpay_order_id")
        signature = data.get("razorpay_signature")

        try:
            payment = Payment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.paid = True
            payment.save()

            return render(request, "hotels/payment_success.html", {"payment": payment})

        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found!"}, status=400)

    return redirect("home")

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room', 'room__hotel')
    return render(request, 'hotels/my_bookings.html', {'bookings': bookings})

def terms_and_conditions(request):
    return render(request, 'hotels/terms_and_conditions.html')