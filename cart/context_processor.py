from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from profile.models import Profile
from .models import Cart


def cart_context(request):
    try:
        profile = Profile.objects.get(user=request.user)
        cart = Cart.objects.get(profile=profile)
        return {'cart': cart}

    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
        cart = Cart.objects.create(profile=profile)
        return {'cart': cart}

    except Cart.DoesNotExist:
        cart = Cart.objects.create(profile=profile)
        return {'cart': cart}

    except:
        return {'cart': 'please login to see your cart!'}
