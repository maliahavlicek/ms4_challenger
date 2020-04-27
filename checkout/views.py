from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from .forms import MakePaymentForm
from django.conf import settings
from products.models import ServiceLevel
from .models import Order
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Profile
import stripe

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request, pk):
    product = ServiceLevel.objects.get(id=pk)
    user = User.objects.get(email=request.user.email)
    if request.method == "POST":
        payment_form = MakePaymentForm(request.POST)
        order = Order(
            user=user,
            product=product,
            total=product.price
        )

        # if payment is nothing, save order and go to profile page
        if product.price == 0:
            order.payment_status = 'payment_collected'
            order.save()
            profile = Profile.objects.get(user=user)
            profile.product_level = product
            profile.save()
            return redirect(reverse('profile'))

        elif payment_form.is_valid():
            order.save()

            try:
                # stripe takes integer amount so need to multiply from cents up
                customer = stripe.Charge.create(
                    amount=int(product.price * 100),
                    currency="USD",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],
                )
            except stripe.error.CardError:
                # user has not paid, update the Order status
                order.payment_status = 'payment_rejected'
                order.save()
                messages.error(request, "Your card was declined!")

            if customer.paid:
                # user has paid, update the Order status
                messages.error(request, "You have successfully paid")
                order.payment_status = 'payment_collected'
                order.save()
                # user has paid, update the Customer object with the product, so they get more features enabled
                profile = Profile.objects.get(user=user)
                profile.product_level = product
                profile.save()
                return redirect(reverse('profile'))
            else:
                # user has not paid, update the Order status
                order.payment_status = 'payment_rejected'
                order.save()
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()

    return render(request, "checkout.html",
                  {'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE, 'product': product, 'customer': user})
