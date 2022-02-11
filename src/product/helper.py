from product.models import Variant, Product, ProductVariant, ProductVariantPrice, ProductImage


def make_product(data, product):
    for image_url in data['product_image']:
        product_image = ProductImage(product=product, file_path=image_url)
        product_image.save()

    for product_variants in data['product_variant']:
        variant = Variant.objects.get(id=product_variants['option'])
        for product_variant_title in product_variants['tags']:
            product_variant_obj = ProductVariant(variant_title=product_variant_title, variant=variant, product=product)
            product_variant_obj.save()

    for product_variant_price in data['product_variant_prices']:
        title_list = product_variant_price['title'].split('/')
        product_variant_price_obj = ProductVariantPrice(product=product, price=product_variant_price['price'],
                                                        stock=product_variant_price['stock'])

        product_variant_one = ProductVariant.objects.filter(product=product, variant_title=title_list[0]).first()
        product_variant_price_obj.product_variant_one = product_variant_one
        product_variant_two = ProductVariant.objects.filter(product=product, variant_title=title_list[1]).first()
        product_variant_price_obj.product_variant_two = product_variant_two
        product_variant_three = ProductVariant.objects.filter(product=product, variant_title=title_list[2]).first()
        product_variant_price_obj.product_variant_three = product_variant_three

        product_variant_price_obj.save()

    response = {
        'status': 201,
        'detail': 'Operation Completed Successfully!'
    }

    return response