from django.db import models

# Модель Категория
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Модель Подкатегория
class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

# Модель Товар
class Products(models.Model):
    photo=models.ImageField(null=True,blank=True,upload_to="images/")
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Banner(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True, upload_to="images/")

class Basket(models.Model):
    user = models.BigIntegerField(unique=True)

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Количество конкретного продукта в корзине
    def __str__(self):
        return f"{self.basket.user} {self.product.name}"
    class Meta:
        unique_together = ('basket', 'product')