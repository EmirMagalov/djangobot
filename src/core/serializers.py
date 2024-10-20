from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BasketItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_photo = serializers.ImageField(source="product.photo")

    # def get_product_photo(self, obj):
    #     request = self.context.get('request')  # Получите объект request из контекста
    #     photo_url = obj.product.photo.url if obj.product.photo else None
    #     return request.build_absolute_uri(photo_url) if request and photo_url else None
    class Meta:
        model = BasketItem
        fields = '__all__'

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)  # Связанные товары с количеством

    class Meta:
        model = Basket
        fields = '__all__'