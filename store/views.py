from django.http import Http404
from django.shortcuts import redirect, render
from .models import Category, Product, Order
from accounts.models import Customer
from .decorators import auth_middlware

def home_view(request):
    page_title = 'Home'
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'page_title': page_title
    }
    if request.method == 'POST':
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else: 
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'], 'tututututuuu')
        return redirect('home')
    return render(request, 'index.html', context)


def cart_view(request):
    context = {}
    page_title = 'Cart'
    if request.session.get('cart'):
        cart_product_slugs = list(request.session.get('cart').keys())
        cart_products = Product.get_products_by_slug(cart_product_slugs)
        print(cart_products)
        context['cart_products'] = cart_products

    context['page_title'] = page_title
    return render(request, 'cart.html', context)

@auth_middlware
def checkout_view(request):
    page_title = 'Checkout'
    context = {}
    if request.method == 'POST':
        region = request.POST.get('region')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        cart = request.session.get('cart')
        customer = Customer(id = request.session.get('customer_id'))
        products = Product.get_products_by_slug(list(cart.keys()))
        values = {'region':region, 'address': address, 'phone': phone}

        error_msg = None
        if not region:
            error_msg = 'Region required'
        elif not address:
            error_msg = 'Address required!'
        elif not phone or len(phone) < 10:
            error_msg = 'Valid phone number required!'
        else:
            for product in products:
                order = Order(customer=customer, product=product, region=region, address=address, phone=phone, quantity=cart.get(product.slug))
                print(address, cart, products, '88888888888')
                order.save()
                update_product(order, product)


            # On successful checkout, clear cart session cookies.
            request.session['cart'] = {}            
            return redirect('cart')
        context = {'customer': customer, 'error_msg': error_msg, 'values':values, 'page_title':page_title}
    return render(request, 'checkout.html', context)

def update_product(order, product):
    product.quantity = product.quantity - order.quantity
    product.save()


@auth_middlware
def order_view(request):
    page_title = 'Orders'
    try:
        customer = request.session.get('customer_id')
        orders = Order.get_order_by_customer(customer)
    except:
        raise Http404
    context = {'orders': orders, 'page_title':page_title}
    print(orders)
    return render(request, 'order.html', context)