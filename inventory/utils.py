from .models import Order


def cartData(request):
    cashier = request.user
    order, created = Order.objects.get_or_create(cashier=cashier, complete=False)
    items = order.orderitem_set.all()
    cartItems = order.get_cart_items

    return {'cartItems': cartItems, 'order': order, 'items': items}
