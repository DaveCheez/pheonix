from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from store.models import Product
from .serializers import CartSerializer
import traceback


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if cart_item.cart.user == request.user:
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
    return redirect('cart:cart')

@api_view(['POST'])
def create_cart(request):
    cart = Cart.objects.create()
    return Response({'cart_id': str(cart.id)})

@api_view(['GET'])
def get_cart(request):
    cart_id = request.query_params.get('cart_id')

    if not cart_id:
        return Response({'error': 'Missing cart_id'}, status=400)

    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)

    items = CartItem.objects.filter(cart=cart)

    cart_items = []
    cart_total = 0

    for item in items:
        unit_price = item.product.price or 0
        line_total = unit_price * item.quantity
        cart_total += line_total

        cart_items.append({
            'item_id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': str(line_total),  # 👈 Total for this line
        })

    return Response({
        'success': True,
        'cart': {
            'id': str(cart.id),
            'items': cart_items,
            'total': str(cart_total),  # 👈 Grand total
        }
    })


@api_view(['POST'])
def add_to_cart(request):
    try:
        cart_id = request.data.get('cart_id')
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        if not cart_id:
            return Response({'error': 'Missing cart_id'}, status=400)

        cart = Cart.objects.get(id=cart_id)

        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()

        return Response({'success': True})
    
    except Exception as e:
        traceback.print_exc()  # Log full stack trace to terminal
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def update_cart_item(request):
    item_id = request.data.get('item_id')
    quantity = int(request.data.get('quantity'))

    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.quantity = quantity
        item.save()
        return Response({'success': True})
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)

@api_view(['POST'])
def remove_from_cart(request):
    item_id = request.data.get('item_id')
    cart_id = request.data.get('cart_id')

    if not item_id or not cart_id:
        return Response({'error': 'Missing item_id or cart_id'}, status=400)

    try:
        item = CartItem.objects.get(id=item_id, cart_id=cart_id)
        item.delete()
        return Response({'success': True})
    except CartItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)


