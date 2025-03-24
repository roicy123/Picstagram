import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Product, Order, CartItem, Payment
from .forms import ProductForm

# ✅ Set API Key
stripe.api_key = settings.STRIPE_SECRET_KEY

# 🔹 Product List View
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

# 🔹 Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

# 🔹 Add Product
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

# 🔹 Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product, defaults={'quantity': 1})

    if not created:
        messages.info(request, 'This product is already in your cart.')
    else:
        messages.success(request, 'Product added to cart!')

    return redirect('cart_view')

# 🔹 View Cart
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'products/cart.html', {'cart_items': cart_items})

# 🔹 Checkout View with Stripe PaymentIntent
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect("cart_view")

    total_amount = sum(item.product.price * item.quantity for item in cart_items) * 100  # Convert to cents

    try:
        print(f"Total amount in cents: {total_amount}")  # Debugging Log

        # ✅ Create an Order before processing payment
        order = Order.objects.create(user=request.user, ordered_at=timezone.now())
        order.items.set(cart_items)  # Associate cart items with the order

        # ✅ Create Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(total_amount),
            currency="usd",
            payment_method_types=["card"],
        )

        # ✅ Store Payment in Database
        payment = Payment.objects.create(
            user=request.user,
            order=order,  # Associate the order with the payment
            amount=total_amount / 100,  # Store in dollars
            stripe_payment_intent_id=intent.id,
            payment_status="Pending",
        )

        return render(request, "products/checkout.html", {
            "client_secret": intent.client_secret,
            "total_price": total_amount / 100,  # Convert cents to dollars
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "payment": payment,
        })

    except stripe.error.StripeError as e:
        print(f"Stripe Error: {str(e)}")  # Debugging Log
        messages.error(request, f"Stripe error: {str(e)}")
        return redirect("cart_view")


# 🔹 Payment Success View
@csrf_exempt
def payment_success(request):
    if request.method == "GET":
        payment_intent_id = request.GET.get("payment_intent")

        if not payment_intent_id:
            return JsonResponse({"status": "Failed", "message": "Missing payment_intent"}, status=400)

        try:
            # ✅ Retrieve and Update Payment Status
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent_id)
            payment.payment_status = "Completed"
            payment.save()

            # ✅ Remove Purchased Products from Database
            order = payment.order
            for cart_item in order.items.all():
                cart_item.product.delete()  # Delete the product from the database

            # ✅ Clear the user's cart after purchase
            CartItem.objects.filter(user=request.user).delete()

            return render(request, "products/payment_success.html", {"payment": payment})

        except Payment.DoesNotExist:
            return JsonResponse({"status": "Failed", "message": "Payment not found"}, status=404)

    return JsonResponse({"status": "Failed"}, status=400)
