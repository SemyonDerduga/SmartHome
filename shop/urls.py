from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^package/$', views.package, name='package'),
    url(r'^assistant_popularity/$', views.assistant_popularity, name='assistant_popularity'),
    url(r'^assistants/$', views.assistants, name='assistants'),
    url(r'^assistant_price/$', views.assistant_price, name='assistant_price'),
    url(r'^cleaners/$', views.cleaners, name='cleaners'),
    url(r'^locks/$', views.locks, name='locks'),
    url(r'^builtin/$', views.builtin, name='builtin'),
    url(r'^sensors/$', views.sensors, name='sensors'),
    url(r'^product/(?P<pk>\d+)/$', views.product_detail, name='product_detail'),
    url(r'^add/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^finish/$', views.close_order, name='finish'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

