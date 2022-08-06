from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    slugs = cart.keys()
    for slug in slugs:
        if slug == product.slug:
            return True
    return False

@register.filter(name='quantity_in_cart')
def quantity_in_cart(product, cart):
    slugs = cart.keys()
    for slug in slugs:
        if slug == product.slug:
            return cart.get(slug)
    return 0

@register.filter(name='total_price')
def total_price(product, cart):
    return product.price * quantity_in_cart(product, cart)

@register.filter(name='grand_product_total')
def grand_product_total(products, cart):
    sum = 0
    for product in products:
        sum += total_price(product, cart)
    return sum

@register.filter(name='currency')
def currency(price):
    return f"Ksh {price:,}"

@register.filter(name='order_item_total')
def order_item_total(quantity, price):
    return quantity * price

@register.filter(name="total_cart_items")
def total_cart_items(total, values):
    for value in values:
        total += value
    return total