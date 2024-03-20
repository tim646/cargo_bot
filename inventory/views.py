from django.db import transaction
from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import datetime
from django.shortcuts import get_object_or_404

from .models import *
from .utils import cartData


# Create your views here.
@login_required
@csrf_exempt
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order_items = data['items']
    total_price = data['order'].get_cart_total
    products = Inventory.objects.filter(quantity__gt=0, on_sale=True)
    order = data['order']
    print(data)
    context = {'products': products, 'cartItems': cartItems, 'order_items': order_items, 'total_price': total_price, 'order': order, 'items': data['items']}
    return render(request, 'store.html', context)


# @csrf_exempt
@login_required
@csrf_exempt
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'cart.html', context)


# @csrf_exempt
@login_required
@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId: ', productId)

    cashier = request.user
    product = Inventory.objects.get(id=productId)
    order, created = Order.objects.get_or_create(cashier=cashier, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if orderItem.quantity < product.quantity:
            orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# @csrf_exempt
@login_required
@csrf_exempt
def processOrder(request):
    data = json.loads(request.body)
    cashier = request.user
    print("order id ", data['orderId'])
    order, created = Order.objects.get_or_create(id=data['orderId'], complete=False)

    total = float(data['total_price'])
    print("printing tot11 ", total)
    print("printing get_card_total ", order.get_cart_total)

    if int(total) == int(order.get_cart_total):
        try:
            with transaction.atomic():
                # reduce quantity of products
                for item in order.orderitem_set.all():
                    product = item.product
                    product.quantity -= item.quantity
                    product.save()
                order.complete = True
                order.save()

        except:
            return JsonResponse('Payment failed', safe=False)

        return JsonResponse('Payment complete!', safe=False)
    else:
        return JsonResponse('Payment failed', safe=False)


# @csrf_exempt
@login_required
@csrf_exempt
def inventory_detail(request, pk):
    data = cartData(request)
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {'inventory': inventory}
    return render(request, 'inventory_detail.html', context)
