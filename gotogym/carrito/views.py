from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product

# Añadir producto al carrito
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_count = sum(cart.values())
        return JsonResponse({'success': True, 'cart_count': cart_count})
    return redirect('carrito:cart_detail')

# Eliminar producto del carrito
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('carrito:cart_detail')

# Actualizar cantidad
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cantidad_actual = cart.get(str(product_id), 1)
        accion = request.POST.get('accion')
        cantidad_input = request.POST.get('cantidad')
        if accion == 'sumar':
            cantidad_actual += 1
        elif accion == 'restar':
            cantidad_actual -= 1
        elif cantidad_input:
            try:
                cantidad_actual = int(cantidad_input)
            except ValueError:
                cantidad_actual = 1
        if cantidad_actual > 0:
            cart[str(product_id)] = cantidad_actual
        else:
            cart.pop(str(product_id), None)
        request.session['cart'] = cart
    return redirect('carrito:cart_detail')

# Mostrar carrito
def cart_detail(request):
    cart = request.session.get('cart', {})
    productos = Product.objects.filter(id__in=cart.keys())
    items = []
    total = 0
    for producto in productos:
        cantidad = cart[str(producto.id)]
        subtotal = producto.price * cantidad
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
        total += subtotal
    shipping = 5 if items else 0
    total_price = total + shipping

    # Mostrar estado de pago de MercadoPago si viene en la URL
    payment_status = request.GET.get('collection_status')
    if payment_status == 'approved':
        messages.success(request, '¡Pago aprobado! Gracias por tu compra.')
        # Limpiar carrito si el pago fue exitoso
        request.session['cart'] = {}
    elif payment_status == 'pending':
        messages.info(request, 'El pago está pendiente. Te notificaremos cuando se acredite.')
    elif payment_status == 'rejected':
        messages.error(request, 'El pago fue rechazado. Intenta nuevamente.')

    return render(request, 'carrito/cart_detail.html', {
        'items': items,
        'total': total,
        'shipping': shipping,
        'total_price': total_price,
        'num_items': sum(cart.values()),
    })
