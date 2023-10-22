from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
app_name = 'eshop'

from eshop.views import home, product, brand, category, search, add_cart_item, cart,cart_add_mini,login


urlpatterns = [
    path('', home, name="homepage"),
    path('product/<int:product_id>/', product, name="product"),
    path('addcartitem/', add_cart_item, name="add_cart_item"),
    path('cart/', cart, name="cart"),
    
    path('pluse/<int:id_pluse>/', cart_add_mini, name="cart_item_plus"),
    path('minus/<int:id_minus>/', cart_add_mini, name="cart_item_minus"),
    path('delete/<int:id_delete>/', cart_add_mini, name="cart_item_delete"),
    
    path('brand/<str:slug>/', brand, name="brand"),
    path('category/<str:slug>/', category, name="category"),
    path('search/<str:slug>/', search, name="search"),
    path('login/', login, name="login"),
    
    
   
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
