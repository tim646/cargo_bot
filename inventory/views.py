from django.shortcuts import render

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
import datetime

from .models import *
from .utils import cartData


# Create your views here.
@csrf_exempt
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Inventory.objects.all()
    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'store.html', context)


@csrf_exempt
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}

    return render(request, 'cart.html', context)




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


@csrf_exempt
def processOrder(request):
    data = json.loads(request.body)
    cashier = request.user
    order, created = Order.objects.get_or_create(id=data['orderId'], complete=False)

    total = float(data['total_price'])
    print("printing tot11 ",total)
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    return JsonResponse('Payment complete!', safe=False)


@csrf_exempt
def inventory_detail(request, pk):
    data = cartData(request)
    inventory = Inventory.objects.get(id=pk)
    context = {'inventory': inventory}
    return render(request, 'inventory_detail.html', context)
