from django.shortcuts import redirect, render, get_object_or_404
from catalog.models import Book
from .cart import Cart
from django.db import transaction
from django.core.mail import send_mail
from .models import OrderItem, Order
from .forms import OrderCreateForm

@transaction.atomic
def order_create(request):

    cart = Cart(request)

    if request.method == 'POST':

        form = OrderCreateForm(request.POST)

        if form.is_valid():

            order = form.save()

            for item in cart:

                OrderItem.objects.create(
                    order=order,
                    book=item['book'],
                    price=item['book'].price,
                    quantity=item['quantity']
                )

            send_mail(
                'Order created',
                f'Your order #{order.id} was created successfully.',
                'admin@example.com',
                [order.email],
                fail_silently=True,
            )

            cart.clear()

            return render(
                request,
                'orders/order_created.html',
                {'order': order}
            )

    else:
        form = OrderCreateForm()

    return render(
        request,
        'orders/order_create.html',
        {
            'cart': cart,
            'form': form
        }
    )


def cart_detail(request):
    cart = Cart(request)

    return render(request, 'orders/cart_detail.html', {
        'cart': cart
    })


def cart_add(request, book_id):
    cart = Cart(request)

    book = get_object_or_404(Book, id=book_id)

    cart.add(book)

    return redirect('orders:cart_detail')


def cart_remove(request, book_id):
    cart = Cart(request)

    book = get_object_or_404(Book, id=book_id)

    cart.remove(book)

    return redirect('orders:cart_detail')