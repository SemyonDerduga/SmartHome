from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import shutil
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=1000, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ProductCategory(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey('shop.ProductCategory')
    number_of_purchases = models.IntegerField(default=0)
    vendor_code = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=10000, blank=True, null=True)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Opened at')
    closed_at = models.DateTimeField(verbose_name='Closed at', blank=True, null=True)
    is_closed = models.BooleanField(default=False, verbose_name='Is closed')
    is_processed = models.BooleanField(default=False, verbose_name='Is processed')
    phone = models.CharField(max_length=32, null=True)
    address = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=64, verbose_name='Contact name', null=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def price(self):
        total_price = 0
        for p in self.positions.all():
            total_price += p.price()
        return total_price


class OrderPosition(models.Model):
    order = models.ForeignKey('Order', related_name='positions')
    product = models.ForeignKey('Product')
    count = models.PositiveIntegerField(default=0)



    class Meta:
        verbose_name = 'Order position'
        verbose_name_plural = 'Order positions'
        ordering = ['-count']

    def price(self):
        return self.product.price * self.count

class Postavshik(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'postavshik'
        verbose_name_plural = 'postavshik'
