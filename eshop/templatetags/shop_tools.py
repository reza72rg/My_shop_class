from django import template

from django.db.models import Sum, F
from django.contrib.humanize.templatetags.humanize import intcomma
from eshop.models import Setting, Category, Cart, CartItem, Discount
from django.utils.translation import gettext_lazy as _


register = template.Library()

persian_digits = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}


@register.simple_tag
def get_setting(setting_name):
    s = Setting.objects.first()
    try:
        # if setting_name == "site_logo":
        #     return s.site_logo.url
        # elif setting_name == "site_title":
        #     return s.site_title
        return getattr(s, setting_name).url
    except:
        return getattr(s, setting_name)


@register.simple_tag
def get_categories():
    return Category.objects.filter(level=0).order_by('title')


@register.filter
def to_persian_number(value):
    value = "".join([persian_digits.get(c, c) for c in value])
    return value


@register.simple_tag
def get_currency():
    currency = "Toman"
    return _(currency)


@register.simple_tag
def cart_items_count(user):
    try:
        c = Cart.objects.get(user=user)
        # count = 0
        # for i in CartItem.objects.filter(cart=c):
        #     count += i.count
        # return count
        return CartItem.objects.filter(cart=c).aggregate(Sum("count"))["count__sum"]
    except:
        return to_persian_number("0")


@register.simple_tag
def product_discount(product):
    try:
        dp = Discount.objects.get(product=product, is_active=True)
        price = product.price
        if not dp.percent == 0:
            return to_persian_number(intcomma(price * (100 - dp.percent) // 100, False))
        else:
            return False
    except:
        return False


@register.simple_tag
def cart_total_price(cart_id):
    c = Cart.objects.get(id=cart_id)
    return to_persian_number(intcomma(CartItem.objects.filter(cart=c).annotate(total_field_price=F('count') * F('price')).aggregate(Sum("total_field_price"))["total_field_price__sum"], False))


@register.simple_tag
def cart_total_price_with_tax(cart_id, tax, discount_price):
    c = Cart.objects.get(id=cart_id)
    return to_persian_number(intcomma(CartItem.objects.filter(cart=c).annotate(total_field_price=F('count') * F('price')).aggregate(Sum("total_field_price"))["total_field_price__sum"] - discount_price + tax, False))










