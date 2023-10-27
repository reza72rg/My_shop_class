from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponseRedirect
from eshop.models import Product, ProductImage, ProductProperty, Discount, Cart, CartItem, ProductMonetaryOption, \
    Setting, ShippingAddress
from eshop.forms import ShippingAddressForm


def home(request):
    # # products = Product.objects.all()
    # products = Product.objects.filter(is_active=True)
    # return render(request, template_name="home.html", context={'products': products})
    products = Product.objects.filter(is_active=True).order_by('category')
    context = {"products": products}
    return render(request, template_name="home_page.html", context=context)


def brand(request, slug):
    context = {"products": Product.objects.filter(is_active=True, brand__title=slug.replace("-", " "))}
    return render(request, template_name="products.html", context=context)


def category(request, slug):
    context = {"products": Product.objects.filter(is_active=True, category__title=slug.replace("-", " "))}
    return render(request, template_name="products.html", context=context)


def product(request, product_id):
    p = get_object_or_404(Product, id=product_id, is_active=True)
    p.view = p.view + 1
    p.save()
    # p = Product.objects.get(id=product_id, is_active=True)
    images = ProductImage.objects.filter(product=product_id)
    options = ProductProperty.objects.filter(product=product_id)
    price = p.price
    additional = ""
    try:
        discount = Discount.objects.get(product=product_id, is_active=True).percent
        price = (p.price // 100) * (100 - discount)
        additional = p.price
    except:
        pass
    context = {"product": p, "images": images, "options": options, "price": price, "additional": additional}
    return render(request, template_name="product.html", context=context)


def search(request, slug):
    q = Q()
    for s in slug.split("-"):
        q &= Q(title__icontains=s) | Q(description__icontains=s)
    products = Product.objects.filter(q, is_active=True)
    context = {"products": products}
    return render(request, template_name="products.html", context=context)


@login_required
def add_cart_item(request):
    product_id = request.POST["product_id"]
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=product_id)
    try:
        discount = Discount.objects.get(product=product_id).percent
    except:
        discount = 0
    if request.POST.get("option_id", ""):
        option = ProductMonetaryOption.objects.get(id=request.POST["option_id"])
        final_price = (product.price//100) * (100-discount) + option.price
        try:
            ci = CartItem.objects.get(cart=cart, product=product, monetary_option=option, price=final_price)
            if ci.monetary_option.count <= ci.count:
                return JsonResponse({"error": _("maximum available products reached")})
            else:
                ci.count += 1
                ci.save()
        except:
            ci = CartItem.objects.create(cart=cart, product=product, monetary_option=option, count=1, price=final_price)
            ci.save()
    else:
        final_price = (product.price//100) * (100-discount)
        try:
            ci = CartItem.objects.get(cart=cart, product=product, price=final_price)
            if ci.product.count <= ci.count:
                return JsonResponse({"error": _("maximum available products reached")})
            else:
                ci.count += 1
                ci.save()
        except:
            ci = CartItem.objects.create(cart=cart, product=product, count=1, price=final_price)
            ci.save()
    data = _("item successfully added to cart")
    return JsonResponse({"success": data})


@login_required
def cart(request,**kwargs):
    try:
        c = Cart.objects.get(user=request.user)
        ci = CartItem.objects.filter(cart=c)              
        dc = c.discount_code
        setting = Setting.objects.first()
        tax = 0
        if setting.has_value_added_tax:
            price = 0
            for item in ci:
                price += item.price * item.count
            tax = price * (100 - dc.percent) // 100 * setting.value_added_tax_percent // 100 \
            if dc else price * setting.value_added_tax_percent // 100  
        if dc:
            discount_price = price * dc.percent // 100
        else:
            discount_price = 0
        context = {"cart_id": c.id, "cart_items": ci, "tax": tax, "discount_price": discount_price}
    except:
        context = {}
    return render (request, "cart.html", context=context)
@login_required
def plus_cart_item(request, cart_item_id):
    c = Cart.objects.get(user=request.user)
    ci = CartItem.objects.get(cart=c, id=cart_item_id)
    try:
        if ci.monetary_option.count <= ci.count:
            return HttpResponseRedirect(f"{reverse('cart')}?error=1")
        else:
            ci.count += 1
            ci.save()
    except:
        if ci.product.count <= ci.count:
            return HttpResponseRedirect(f"{reverse('cart')}?error=1")
        else:
            ci.count += 1
            ci.save()
    return HttpResponseRedirect(reverse("cart"))


@login_required
def minus_cart_item(request, cart_item_id):
    c = Cart.objects.get(user=request.user)
    ci = CartItem.objects.get(cart=c, id=cart_item_id)
    ci.count -= 1
    if ci.count <= 0:
        pass
    else:
        ci.save()
    return HttpResponseRedirect(reverse("cart"))


@login_required
def del_cart_item(request, cart_item_id):
    c = Cart.objects.get(user=request.user)
    CartItem.objects.get(cart=c, id=cart_item_id).delete()
    if len(CartItem.objects.filter(cart=c)) == 0:
        c.delete()
    return HttpResponseRedirect(reverse("cart"))
@login_required
def shipp_payment(request):
    shipping_instance = None
    try:
        shipping_instance = ShippingAddress.objects.get(user=request.user)
    except:
        pass
    shipping_address_form = ShippingAddressForm(instance=shipping_instance)
    c = Cart.objects.get(user=request.user)
    ci = CartItem.objects.filter(cart=c)
    # ps = []
    # for i in ci:
    #     ps.append(i.product)
    ps = [i.product for i in ci]
    sm_dict = {}
    sm_list = []
    for product in ps:
        for method in product.shipping_methods.all():
            if method in sm_dict:
                sm_dict[method] += 1
            else:
                sm_dict[method] = 1
    for k, v in sm_dict.items():
        if v == len(ps):
            sm_list.append(k)
    return render(request=request, template_name="shipp_payment.html",
                  context={"shipping_address_form": shipping_address_form,
                           "shipping_methods": sm_list})

