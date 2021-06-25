from rest_framework import routers, serializers, viewsets
from cart.models import Cart


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = ['profile', 'product',
                  'items', 'total_price', 'total_number',
                  'order_id']


class CartViewSer(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


router = routers.DefaultRouter()
router.register(r'carts', CartViewSer)
