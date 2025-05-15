from rest_framework import serializers
from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    brands = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'brands', 'categories']

    def get_brands(self, obj):
        # returns a list of dicts: [{id:1, name:"Brand A"}, …]
        return list(obj.brands.values('id', 'name'))

    def get_categories(self, obj):
        return list(obj.categories.values('id', 'name'))
