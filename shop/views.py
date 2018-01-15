from django.shortcuts import render, get_object_or_404

from django.utils import timezone

from django.shortcuts import redirect

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from shop.models import Product, ProductCategory, User

import datetime
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from shop.models import Order, OrderPosition
from shop.forms import AddToCartForm, OrderForm, OrderPositionFormset

from .models import Product


# Create your views here.

def home_page(request):
    content = {
        'product': Product.objects.all(),
        'active_main': "active",
        'quantity': Product.objects.all().__len__() % 3,

    }
    # product = Product.objects.all()
    # print(product.__len__())
    return render(request, 'shop/home_page.html', content)


def assistants(request):
    content = {
        'product': Product.objects.filter(category__name="Assistants"),
        'active_main': "active",
        'quantity': Product.objects.filter(category__name="Assistants").__len__() % 3,

    }
    return render(request, 'shop/categories/Assistants.html', content)

def assistant_popularity(request):
    content = {
        'product': reversed(Product.objects.filter(category__name="Assistants").order_by("number_of_purchases")),
        'active_main': "active",
        'quantity': Product.objects.filter(category__name="Assistants").__len__() % 3,

    }
    return render(request, 'shop/categories/Assistent_popularity.html', content)

def assistant_price(request):
    content = {
        'product': reversed(Product.objects.filter(category__name="Assistants").order_by("price")),
        'active_main': "active",
        'quantity': Product.objects.filter(category__name="Assistants").__len__() % 3,

    }
    return render(request, 'shop/categories/Assistant_price.html', content)


def builtin(request):
    content = {
        'product': Product.objects.filter(category__name="Builtin"),
        'active_main': "active",
        'quantity': Product.objects.filter(category__name="Builtin").__len__() % 3,

    }
    return render(request, 'shop/categories/Builtin.html', content)


def cleaners(request):
    content = {
        'product': Product.objects.filter(category__name="Cleaners"),
        'active_main': "active",
        'quantity': Product.objects.filter(category__name="Cleaners").__len__() % 3,

    }
    return render(request, 'shop/categories/Cleaners.html', content)


def locks(request):
    content = {
        'product': Product.objects.filter(category__name="Locks"),
        'active_main': "active",
        'quantity': Product.objects.filter(category__name="Locks").__len__() % 3,

    }
    return render(request, 'shop/categories/Locks.html', content)


def sensors(request):
    content = {
        'product': Product.objects.filter(category__name="Sensors"),
        'active_main': "active",
        'quantity': Product.objects.filter(category__name="Sensors").__len__() % 3,

    }
    return render(request, 'shop/categories/Sensors.html', content)


def package(request):
    content = {
        'product': [Product.objects.get(title="Hue White and color ambiance Starter kit E26"),
                    Product.objects.get(title="Xiaomi Умный дом Комплект"),
                    Product.objects.get(title="Google Home"),

                    ],
        'active_package': "active",
        'quantity': Product.objects.all().__len__() % 3,

    }
    return render(request, 'shop/package.html', content)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def get_order(request):
    order_id = request.session.get('order_id')
    order = None
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            pass
    return order


def add_to_cart(request):
    order = get_order(request)
    if not order:
        order = Order.objects.create()
        request.session['order_id'] = order.id
    form = AddToCartForm(request.POST)
    if form.is_valid():
        product = form.cleaned_data['product']
        order_position, created = OrderPosition.objects.get_or_create(
            product=product,
            order=order,
        )
        order_position.count += 1
        order_position.save()
    print(form.errors)
    return redirect('cart')


def close_order(request):
    if request:
        order = get_order(request)
        order.is_closed = True

        order.save()
        return render(request, 'shop/close_order.html', {
            'order': order,
        })
    else:
        return redirect('order')


def cart(request):
    price = 0.0
    order = get_order(request)
    for tovar in order.positions.all():
        price = price + float(tovar.product.price) * float(tovar.count)

    if not order:
        order = Order.objects.create()
        request.session['order_id'] = order.id
        price = 0.0
        for tovar in order.positions.all():
            price = price + float(tovar.product.price) * float(request.POST["count_" + tovar.product.title])
    if request.POST:

        if request.POST.get("close_order", False) == "Заказать":
            id = order.id
            user = request.user
            order.is_closed = True
            user.is_active = False
            user.first_name = request.POST["user_name"]
            user.last_name = request.POST["user_surname"]
            if request.user.is_authenticated():
                user.profile.address = request.POST["address"]
                user.profile.phone_number = request.POST["user_phone"]
                user.is_active = True
                user.save()
            order.name = request.POST["user_name"] + ' ' + request.POST["user_surname"]
            order.address = request.POST["address"]
            order.phone = request.POST["user_phone"]
            price = 0.0
            for tovar in order.positions.all():
                tovar.count = int(request.POST["count_" + tovar.product.title])
                tovar.save()
                price = price + float(tovar.product.price) * float(request.POST["count_" + tovar.product.title])
            order.closed_at = datetime.datetime.now()
            price = 0.0
            for tovar in order.positions.all():
                prod = tovar.product
                prod.number_of_purchases = tovar.product.number_of_purchases + int(request.POST[
                    "count_" + tovar.product.title])
                prod.save()
                price = price + float(tovar.product.price) * float(request.POST["count_" + tovar.product.title])
            order.save()
            order = Order.objects.create()
            request.session['order_id'] = order.id



            return render(request, 'shop/close_order.html', {'order': id})

        print(request.POST["user_name"])
        print(request.POST["user_surname"])
        print(request.POST["user_phone"])
        user = request.user
        user.is_active = False

        user.first_name = request.POST["user_name"]
        user.last_name = request.POST["user_surname"]
        user.profile.address = request.POST["address"]
        user.profile.phone_number = request.POST["user_phone"]
        user.is_active = True
        user.save()
        order.name = request.POST["user_name"] + ' ' + request.POST["user_surname"]
        order.address = request.POST["address"]
        order.phone = request.POST["user_phone"]
        price = 0.0
        for tovar in order.positions.all():

            tovar.count = int(request.POST["count_" + tovar.product.title])
            tovar.save()
            price = price + float(tovar.product.price) * float(request.POST["count_" + tovar.product.title])
            if request.POST.get("delete_" + tovar.product.title, False) == "Удалить":
                print("Удалил " + tovar.product.title)
                tovar.delete()

        order.save()

    content = {
        'order': order,
        'tovaru': order.positions.all(),
        'product': Product.objects.all(),
        'price': str(round(price, 2)),
    }

    print()

    return render(request, 'shop/NewCart.html', content)


class OrderDetails(UpdateView):
    model = Order
    template_name = 'shop/cart.html'
    form_class = OrderForm
    success_url = '/finish'

    def get_object(self, queryset=None):
        return get_order(self.request)

    def get_formset(self):
        return OrderPositionFormset(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = self.get_formset()
        return data

    def form_valid(self, form):
        formset = self.get_formset()
        if formset.is_valid():
            for position_form in formset:
                position_form.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ShopMixin(object):
    """Adds categories and current order to render context"""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        categories = ProductCategory.objects.all()
        data['categories'] = categories
        data['order'] = get_order(self.request)
        return data


class ProductList(ShopMixin, ListView):
    model = Product
    paginate_by = 16
    template_name = 'product_list.html'
    context_object_name = 'products'

    def __init__(self, *args, **kwargs):
        self.category = None
        super().__init__(*args, **kwargs)

    def get_category(self):
        category_id = self.kwargs.get('category_id')
        category = None
        if category_id:
            category = get_object_or_404(
                ProductCategory,
                id=category_id,
            )
            self.category = category
        return category

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.category:
            self.get_category()
        if self.category:
            queryset = queryset.filter(
                category=self.category,
            )
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['selected_category'] = self.get_category()
        return data


class ProductDetailed(ShopMixin, DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
