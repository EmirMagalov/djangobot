from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        id = request.query_params.get('subcategory', None)
        if id:
            self.queryset = self.queryset.filter(subcategory=id)
        return super().list(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserBasketProducts(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        ids = request.query_params.getlist('id')
        print(f"Received IDs: {ids}")  # Логируем полученные идентификаторы
        if ids:
            ids = [int(i) for i in ids]
            self.queryset = self.queryset.filter(id__in=ids)
            print(f"Filtered queryset: {self.queryset}")  # Логируем отфильтрованный queryset
        return super().list(request, *args, **kwargs)

class OneProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    def list(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id:
            self.queryset = self.queryset.filter(id=id)
        return super().list(request, *args, **kwargs)

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    def list(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id:
            self.queryset = self.queryset.filter(category=id)
        return super().list(request, *args, **kwargs)

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def list(self, request, *args, **kwargs):
        name = request.query_params.get('name', None)
        if name:
            self.queryset = self.queryset.filter(name=name)
        return super().list(request, *args, **kwargs)

class BasketListViewSet(APIView):
    def get(self, request, user_id):
        products = BasketItem.objects.filter(basket__user=user_id)  # Фильтруем по user_id
        serializer = BasketItemSerializer(products, many=True)  # Используем BasketItemSerializer
        return Response(serializer.data)

    def post(self, request):
        user_id = request.data.get('user')  # Извлекаем user_id из данных запроса
        product_id = request.data.get('product_id')  # Извлекаем product_id
        quantity = request.data.get('quantity', 1)  # Извлекаем quantity, по умолчанию 1

        # Получение или создание корзины для пользователя
        basket, created = Basket.objects.get_or_create(user=user_id)

        # Попробуем получить элемент корзины
        basket_item, item_created = BasketItem.objects.get_or_create(
            basket=basket,
            product_id=product_id,
            defaults={'quantity': 1}
        )

        # Если элемент уже существует, обновляем количество
        if not item_created:
            basket_item.quantity += quantity  # Увеличиваем количество
            basket_item.save()  # Сохраняем изменения

        return Response({'message': 'Товар успешно добавлен в корзину',
                         'item': {'product_id': product_id, 'quantity': basket_item.quantity}},
                        status=status.HTTP_200_OK)




    # def put(self, request, user_id):
    #     try:
    #         basket = Basket.objects.get(user=user_id)  # Получаем корзину по ID пользователя
    #     except :
    #         return Response({"error": "Basket not found."}, status=status.HTTP_404_NOT_FOUND)
    #
    #     # Здесь вы можете добавить логику для добавления product_id в существующий список
    #     # Например, если поле `product_id` является полем ManyToMany
    #     my_pr=[i.id for i in basket.product_id.all()]
    #     basket.quantity+=1
    #     basket.save()
    #
    #     product_ids = request.data.get("product_id", [])
    #
    #     basket.product_id.add(*product_ids)  # Добавляем новые product_id
    #
    #     # Сериализуем обновленную корзину и возвращаем её
    #     serializer = BasketSerializer(basket)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        # Получаем корзину по ID пользователя
        try:
            basket = Basket.objects.get(user=user_id)
        except Basket.DoesNotExist:
            return Response({"error": "Basket not found."}, status=status.HTTP_404_NOT_FOUND)

        # Удаляем товар из корзины
        try:
            product_id = request.data.get("product_id")
            if product_id is None:
                return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Найти элемент корзины по basket и product
            basket_item = BasketItem.objects.get(basket=basket, product_id=product_id)
            basket_item.delete()  # Удаляем элемент из корзины

        except BasketItem.DoesNotExist:
            return Response({"error": "Product not found in the basket."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Product removed from basket."}, status=status.HTTP_200_OK)
class PlusMinusViews(APIView):
    def put(self, request, user_id):
        try:
            # Получаем корзину по ID пользователя
            basket = Basket.objects.get(user=user_id)
        except Basket.DoesNotExist:
            return Response({"error": "Basket not found."}, status=status.HTTP_404_NOT_FOUND)

        # Извлекаем product_id из запроса
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Получаем элемент корзины по product_id
            basket_item = BasketItem.objects.get(basket=basket, product_id=product_id)
        except BasketItem.DoesNotExist:
            return Response({"error": "Basket item not found."}, status=status.HTTP_404_NOT_FOUND)

        # Логика увеличения или уменьшения количества
        if request.data.get("plus"):
            basket_item.quantity += 1
            basket_item.save()
        elif request.data.get("minus"):
            if basket_item.quantity > 1:  # Предотвращаем отрицательное количество
                basket_item.quantity -= 1
                basket_item.save()
            else:
                return Response({"error": "Quantity cannot be less than 1."}, status=status.HTTP_400_BAD_REQUEST)

        # Возвращаем обновленное количество товара
        return Response({"product_id": product_id, "quantity": basket_item.quantity}, status=status.HTTP_200_OK)

        # product_ids = request.data.get("product_id", [])
        #
        # basket.product_id.add(*product_ids)  # Добавляем новые product_id

        # Сериализуем обновленную корзину и возвращаем её


    # def get(self, request):
    #     products = Product.objects.all()
    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
