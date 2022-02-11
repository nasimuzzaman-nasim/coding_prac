import math
import json
from django.views import generic
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from product.models import Variant, Product, ProductVariant, ProductVariantPrice, ProductImage
from product.helper import make_product


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

    def post(self, request):
        try:
            data = json.loads(request.body)
            product = Product(title=data['title'], sku=data['sku'], description=data['description'])
            product.save()

            response = make_product(data, product)

        except Exception as e:
            response = {
                'status': 400,
                'detail': str(e.args[0])
            }

        return JsonResponse(response, safe=False)


class UpdateProductView(generic.TemplateView):
    template_name = 'products/update.html'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, pk, **kwargs):
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['variants'] = list(variants.all())
        context['product_id'] = pk
        return context

    def post(self, request, pk):
        try:
            data = json.loads(request.body)
            product = Product.objects.get(id=pk)
            product.title = data['title']
            product.sku = data['sku']
            product.description = data['description']
            product.save()

            product.productvariantprice_set.all().delete()
            product.productimage_set.all().delete()

            response = make_product(data, product)
        except Exception as e:
            response = {
                'status': 400,
                'detail': str(e.args[0])
            }

        return JsonResponse(response, safe=False)


class ProductListView(generic.list.ListView):
    model = Product
    template_name = 'products/list.html'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['variants'] = Variant.objects.all()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        query = {}
        title = self.request.GET.get('title')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')
        variant = self.request.GET.get('variant')

        if title:
            query['title__icontains'] = title
        query['productvariantprice__price__range'] = [price_from if price_from else 0, price_to if price_to else math.inf]
        if date:
            query['created_at__date'] = date
        if variant:
            query['productvariant__id'] = variant
        return qs.filter(**query).distinct()


