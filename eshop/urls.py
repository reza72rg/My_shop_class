from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from eshop.views import home, product, brand, category, search, add_cart_item, plus_cart_item, minus_cart_item, \
    del_cart_item, shipp_payment, cart, shipping_address, create_factor, print_factor, factor, \
    login_user,logout_user,register_user,send_sms_code,compare


urlpatterns = [
    path('', home, name="homepage"),
    path('login/', login_user,),
    path('logout/', logout_user,),
    path('register/', register_user,),
    path('send-sms-code/', send_sms_code,),
    path('product/<int:product_id>/', product, name="product"),
    path('addcartitem/', add_cart_item, name="add_cart_item"),
    path('pluscartitem/<int:cart_item_id>/', plus_cart_item, name="cart_item_plus"),
    path('minuscartitem/<int:cart_item_id>/', minus_cart_item, name="cart_item_minus"),
    path('delcartitem/<int:cart_item_id>/', del_cart_item, name="delete_cart_item"),
    path('shipp-payment/', shipp_payment, name="shipp_payment"),
    path('shipping-address/', shipping_address, name="shipping_address"),
    path('create-factor/', create_factor, name="create_factor"),
    path('cart/', cart, name="cart"),
    path('compare/<int:product_id/', compare, name="compare"),
    path('factor/<str:uuid>',factor, name = "factor"),
    path('brand/<str:slug>/', brand, name="brand"),
    path('category/<str:slug>/', category, name="category"),
    path('search/<str:slug>/', search, name="search"),
    path('print-factor/<str:factor_id>/', print_factor, name ="print_factor"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
