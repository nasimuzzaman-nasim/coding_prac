from rest_framework import serializers
from product.models import *


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = [
            'id',
            'title'
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    variant = VariantSerializer()

    class Meta:
        model = ProductVariant
        fields = [
            'variant_title',
            'variant'
        ]


class ProductVariantPriceSerializer(serializers.ModelSerializer):
    product_variant_one = ProductVariantSerializer()
    product_variant_two = ProductVariantSerializer()
    product_variant_three = ProductVariantSerializer()

    class Meta:
        model = ProductVariantPrice
        fields = [
            'product_variant_one',
            'product_variant_two',
            'product_variant_three',
            'price',
            'stock'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'file_path'
        ]


class ProductSerializer(serializers.ModelSerializer):
    productvariantprice_set = ProductVariantPriceSerializer(many=True)
    productimage_set = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'title',
            'sku',
            'description',
            'productvariantprice_set',
            'productimage_set'
        ]