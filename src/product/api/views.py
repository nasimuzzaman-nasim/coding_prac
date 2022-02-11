from rest_framework.generics import RetrieveAPIView

from product.api.serializers import ProductSerializer
from product.models import Product


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'