from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'banner', BannerViewSet)
router.register(r'subcategory', SubCategoryViewSet)
router.register(r'oneproduct', OneProductViewSet,basename='oneproduct')
urlpatterns = [
    path('', include(router.urls)),
    path('add_basket/', BasketListViewSet.as_view(), name='add_basket'),
    path('update_basket/<int:user_id>/', BasketListViewSet.as_view(), name='update_basket'),
    path('plusminus/<int:user_id>/', PlusMinusViews.as_view(), name='plusminus'),
    path('get_basket/<int:user_id>/', BasketListViewSet.as_view(), name='get_basket'),
    path('userbasket/', UserBasketProducts.as_view({'get': 'list'}),name="userbasket"),
]