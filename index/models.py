from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=32)
    create_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.category_name)


class Product(models.Model):
    product_name = models.CharField(max_length=128)
    product_description = models.TextField(blank=True)
    product_price = models.FloatField()
    product_count = models.IntegerField()
    product_photo = models.ImageField(upload_to='media')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  str(self.product_name)


class Cart(models.Model):
    user_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_pr_amount = models.IntegerField()

    def __str__(self):
        return str(self.user_id)