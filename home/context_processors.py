def cart_context(request):
    """Add cart information to all templates"""
    cart = request.session.get('cart', [])
    total_items = sum(item['quantity'] for item in cart)
    cart_count = len(cart)
    
    return {
        'cart_item_count': total_items,
        'cart_count': cart_count
    }


#this is used here for updating the cart count in each and every template 