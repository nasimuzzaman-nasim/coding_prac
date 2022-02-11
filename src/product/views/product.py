import math
from django.views import generic, View

from product.models import Variant, Product, ProductVariant


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


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


