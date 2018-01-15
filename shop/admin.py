from django.contrib import admin
from .models import Product
from .models import ProductCategory
from shop.models import Order, OrderPosition, Profile, Postavshik

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Profile)
admin.site.register(Postavshik)



class OrderPositionInline(admin.TabularInline):
    model = OrderPosition


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderPositionInline,
    ]
    readonly_fields = ['created_at', 'closed_at']


admin.site.register(Order, OrderAdmin)
