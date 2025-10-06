from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductImage, CategoryImage, Review, Cart, CartItem, ProductOption
from rest_framework import generics
from .serializers import ProductSerializer, CategorySerializer, CategoryWithProductsSerializer, ReviewSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def categories(request):
    return {
        'categories': Category.objects.all()
    }

def get_products(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.productimage_set.all()
    context = {
        'product': product,
        'images': images
    }
    return render(request, 'store/products/single.html', context)


def about(request):
    return render(request, 'store/about.html')

class ProductDetailAPI(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class CategoryListAPI(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category_type = self.request.query_params.get('type', 'product')
        return Category.objects.filter(type=category_type)

class CategoryDetailAPI(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryWithProductsSerializer
    lookup_field = 'slug'

class ReviewListAPI(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

@csrf_exempt
def create_cart(request):
    if request.method == 'POST':
        cart = Cart.objects.create()
        return JsonResponse({'cart_id': cart.id})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_id = data.get('cart_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        options = data.get('options', {})

        cart = get_object_or_404(Cart, id=cart_id)
        product = get_object_or_404(Product, id=product_id)

        # Try to find an existing cart item for this product and options
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            # You might need a more sophisticated way to match options
            # For now, we assume options can be matched this way if they are simple.
            # This part of the logic depends heavily on your ProductOption model structure.
            # A more robust solution would involve hashing the selected options.
        )

        if created:
            cart_item.quantity = quantity
        else:
            # If the item already exists, just increase the quantity
            cart_item.quantity += quantity
        
        cart_item.save()

        # If you have ProductOption selections, you would add them to the cart_item here.
        # For example:
        # for group_id, option_id in options.items():
        #     option = get_object_or_404(ProductOption, id=option_id)
        #     cart_item.options.add(option)

        return JsonResponse({'status': 'success', 'cart_item_id': cart_item.id})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_cart(request):
    cart_id = request.GET.get('cart_id')
    cart = get_object_or_404(Cart, id=cart_id)
    # This requires a serializer for your Cart model
    # from .serializers import CartSerializer
    # serializer = CartSerializer(cart)
    # return JsonResponse({'cart': serializer.data})
    return JsonResponse({'cart': {'id': cart.id, 'items': list(cart.items.values('id', 'product__name', 'quantity')), 'total': str(cart.get_total())}})