from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json

from .models import Restaurant, FoodItem, Order
from .forms import FoodItemForm

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))

@login_required
def restaurant_list(request):
    """List all restaurants."""
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant/restaurant_list.html', {'restaurants': restaurants})

@login_required
def restaurant_detail(request, restaurant_id):
    """Display restaurant details along with its food items."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    food_items = restaurant.food_items.all()
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant, 'food_items': food_items})


@login_required
def order_food(request, food_id):
    """Handles food ordering process."""
    food = get_object_or_404(FoodItem, id=food_id)

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        payment_option = request.POST.get("payment")

        # Check if user is staying in a hotel
        is_hotel_stay = "hotel_stay" in request.POST
        location = None if is_hotel_stay else request.POST.get("location")
        hotel_name = request.POST.get("hotel_name") if is_hotel_stay else None
        hotel_location = request.POST.get("hotel_location") if is_hotel_stay else None
        room_number = request.POST.get("room_number") if is_hotel_stay else None
        quantity = int(request.POST.get("quantity", 1))  # Get quantity

        total_price = food.price * quantity  # Calculate total price

        order = Order.objects.create(
            user=request.user,
            food_item=food,
            quantity=quantity,
            total_price=total_price,
            location=location,
            hotel_name=hotel_name,
            hotel_location=hotel_location,
            room_number=room_number,
            payment_status="Pending",
        )

        if payment_option == "online":
            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                "amount": int(order.total_price * 100),
                "currency": "INR",
                "payment_capture": "1",
            })
            order.razorpay_order_id = razorpay_order["id"]
            order.save()

            return render(request, "restaurant/checkout.html", {
                "order": order,
                "razorpay_key": settings.RAZORPAY_API_KEY,
                "razorpay_order_id": order.razorpay_order_id,
                "amount": order.total_price,
                "razorpay_amount": int(order.total_price * 100),
            })

        else:  # Handle Cash on Delivery (COD)
            order.payment_status = "COD"
            order.save()
            messages.success(request, "Your order has been placed successfully!")
            return redirect("order_success")  # Redirect for COD

    # Handle GET request properly
    return render(request, "restaurant/order_food.html", {"food": food})


@csrf_exempt
def order_success(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        
        order.payment_status = "Paid"
        order.save()

        return render(request, "restaurant/order_success.html", {"order": order})


    elif request.method == "GET":
        return render(request, "restaurant/order_success.html")

    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def add_food_item(request, restaurant_id):
    """Allows restaurant owners to add food items to their restaurant."""
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.restaurant = restaurant
            food_item.save()
            messages.success(request, "Food item added successfully!")
            return redirect('restaurant_detail', restaurant_id=restaurant.id)
        else:
            messages.error(request, "Error adding food item. Please check your input.")
    else:
        form = FoodItemForm()

    return render(request, 'restaurant/add_food_item.html', {'form': form, 'restaurant': restaurant})


@csrf_exempt
def verify_payment(request):
    """Verifies payment success from Razorpay."""
    if request.method == "POST":
        data = json.loads(request.body)

        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        try:
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})

        params = {
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params)
            order.payment_status = "Paid"
            order.payment_option = "Online"
            order.save()
            return JsonResponse({"success": True})
        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"success": False, "error": "Signature verification failed"})

    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required
def my_orders(request):
    """Displays the user's past orders."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'restaurant/my_orders.html', {'orders': orders})



