from django.urls import path

from .views import ProductDetailView


urlpatterns = [
    path('product-detail/<pk>', ProductDetailView.as_view(), name='detail.product.api')
]