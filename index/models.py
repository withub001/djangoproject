from django.db import models


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=32) # Название категории
    create_date = models.DateTimeField(auto_now_add=True) # Дата добавления

    def __str__(self):
        return str(self.category_name)


class Product(models.Model):
    product_name = models.CharField(max_length=128) # Название товара
    product_des = models.TextField(blank=True) # Описание товара
    product_price = models.FloatField() # Цена товара
    product_count = models.IntegerField() # Кол-во на складе
    product_photo = models.ImageField(upload_to='media') # Фото товара
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE) # Связь с категорией
    create_date = models.DateTimeField(auto_now_add=True) # Дата добавления

    def __str__(self):
        return str(self.product_name)


class Cart(models.Model):
    user_id = models.IntegerField() # ID пользователя
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE) # Товар, который взял пользователь
    user_pr_amount = models.IntegerField() # Сколько товара взял пользователь

    def __str__(self):
        return str(self.user_id)