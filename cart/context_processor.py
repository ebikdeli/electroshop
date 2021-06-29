from django.shortcuts import get_object_or_404
from .models import Cart


def cart_context(request):
    try:
        cart = get_object_or_404(Cart, id=request.user.profile.profile_cart.id)
        return {'cart': cart}
    except Cart.DoesNotExist:
        return {'cart': 'please login to see your cart!'}
    except AttributeError:
        return {'cart': 'please login to see your cart!'}
