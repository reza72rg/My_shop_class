from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from unidecode import unidecode
from django.contrib.auth import logout,login
from django.contrib.auth.models import User
import random
import requests
import json

from eshop.forms import ShippingAddressForm
from eshop.models import Product, ProductImage, ProductProperty, Discount, Cart, CartItem, ProductMonetaryOption, \
    Setting, ShippingAddress, PaymentMethod, PaymentStatus, ShippingMethod, ShippingCost, ShippingStatus, Factor, \
    FactorItem ,Smsverificationcode
from eshop.templatetags.shop_tools import cart_total_price, cart_total_price_with_tax


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
def cart(request):
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
    return render(request, "cart.html", context=context)


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
        ci.delete()
        if len(CartItem.objects.filter(cart=c)) == 0:
            c.delete()
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
                           "shipping_methods": sm_list
                           })


def shipping_address(request):
    shipping_instance = None
    try:
        shipping_instance = ShippingAddress.objects.get(user=request.user)
    except:
        pass
    shipping_address_form = ShippingAddressForm(data=request.POST or None,
                                                instance=shipping_instance,
                                                initial={'user': request.user})
    shipping_address_form.user = request.user
    if request.method == "POST":
        if shipping_address_form.is_valid():
            shipping_address_form.user = request.user
            shipping_address_form.save()
            messages.success(request, _("shipping address updated"))
        else:
            messages.error(request, _("error updating shipping address"))

    return render(request=request,
                  template_name="shipping_address.html",
                  context={"shipping_address_form": shipping_address_form})


@login_required
def create_factor(request):
    if request.method == "POST":
        try:
            c = Cart.objects.get(user=request.user)
            ci = CartItem.objects.filter(cart=c)
            dc = c.discount_code
            setting = Setting.objects.first()
            tax = 0
            discount_price = 0
            if setting.has_value_added_tax:
                price = 0
                for item in ci:
                    price += item.price * item.count
                tax = price * (100 - dc.percent) // 100 * setting.value_added_tax_percent // 100 if dc else price * setting.value_added_tax_percent // 100
            if dc:
                discount_price = price * dc.percent // 100
        except Exception:
            pass
        price = int(unidecode(str(cart_total_price(c.id))).replace(",", ""))
        total_weight = 0
        is_changed = 0
        for item in ci:
            total_weight += item.product.weight * item.count
            try:
                if item.monetary_option.count <= item.count:
                    is_changed == 1
                    if item.monetary_option.count == 0:
                        item.delete()
                    else:
                        item.count = item.monetary_option.count
                        item.save()
            except:
                if item.product.count <= item.count:
                    is_changed == 1
                    if item.product.count == 0:
                        item.delete()
                    else:
                        item.count = item.product.count
                        item.save()
        if is_changed == 1:
            return JsonResponse({"cart_is_changed": _("cart has changed")})
        payment_method = PaymentMethod.objects.get(code=request.POST["payment_method"])
        payment_status = PaymentStatus.objects.get(code=1)
        shipping_method = ShippingMethod.objects.get(code=request.POST["shipping_method"])
        try:
            sa = ShippingAddress.objects.get(user=request.user)
            if not sa.title:
                return JsonResponse({"error": _("complete the postal information")})
        except:
            return JsonResponse({"error", _("complete the postal information")})
        try:
            shipping_cost = int(unidecode(str(ShippingCost.objects.get(from_weight__gte=total_weight,
                                                                       to_weight__lt=total_weight,
                                                                       states=sa.state).price)).replace(",", ""))
        except:
            shipping_cost = 0
        shipping_status = ShippingStatus.objects.get(code=1)
        final_price = int(unidecode(str(cart_total_price_with_tax(c.id, tax, discount_price))).replace(",", ""))
        f = Factor.objects.create(
            user=request.user,
            price=price,
            value_added_tax=tax,
            discount_code=dc.code if dc else "-----",
            discount_price=discount_price,
            payment_method=payment_method,
            payment_status=payment_status,
            total_weight=total_weight,
            final_price=final_price,
            shipping_method=shipping_method,
            shipping_cost=shipping_cost,
            shipping_status=shipping_status,
            name_family=sa.receiver,
            phone_number=sa.phone,
            state=sa.state,
            city=sa.city,
            address=sa.address,
            post_code=sa.postcode,
            customer_comment=sa.description
        )
        f.save()
        for item in ci:
            item.product.count -= item.count
            item.product.save()
            try:
                item.monetary_option.count -= item.count
            except:
                pass
            fi = FactorItem.objects.create(
                factor=f,
                product=str(item.product),
                monetary_option=str(item.monetary_option if item.monetary_option else ""),
                count=int(item.count),
                price=int(item.price)
            )
            fi.save()
        c.delete()
        return JsonResponse({"success": f.uuid})
    else:
        return JsonResponse({"error": _("error")})
@login_required
def print_factor(request,factor_id):
    return HttpResponseRedirect(reverse("admin:eshop_factor_changelist"))

@login_required
def factor(request,uuid):
    try:
        f = Factor.objects.get(uuid=uuid,  user=request.user)
        fi = FactorItem.objects.filter(factor = f)
        banks = settings.BANKS
        print(banks)
        return render (request= request, template_name="factor.html",context={"factor":f, "factor_items": fi, "banks":banks})
    except:
        return render(request=request, template_name="factor.html",context={"error":_("this factor does not exist!")})

def random_password(lenght=6, with_letter = False , with_symbols = False):
    lower = "abcdefghijklmnoqrstuvwxyz"
    upper = lower.upper()
    numbers = "09107784928"
    symbols = "@#$&_-()+%*:/!?+."
    srting = numbers
    if with_letter:
        srting += lower + upper
    if with_symbols:
        srting += symbols
    return "".join(random.sample(srting, lenght))

def send_sms_code(request):
    if request.POST:
        activation_code = str(random_password())
        mobile = request.POST["mobile_number"]
        ev = Smsverificationcode(mobile = mobile,activation_code= activation_code )
        ev.save()
        # send sms 
        headers ={ 'Context-type ':'applications/json'}
        payload = {'jsonrpc':'2.0', 'method': 'sendsms',
                   'params':{
                       'username': '09107784928',
                       "password": "123456",
                       "special_number":"300224000",
                       "message": f" کد ورود به فروشگاه : {activation_code}",
                       "receivers" : [mobile],
                       "id" : "1",
                       }}
        response = requests.post("https://soomsoft.com/payama/api/rpc/v1/", headers=headers,data=json.dumps(payload)).json()
        return JsonResponse({"success":response} )
        # end send sms
    return HttpResponseRedirect("/")

   
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_user(request):
    contex = dict()
    if request.POST:
        mobile = request.POST.get("mobile_number","")
        sms_code = request.POST.get("sms_code","")
        # check_code
        try:
            if sms_code and mobile:
                ev = Smsverificationcode.objects.get(mobile=mobile,activation_code =sms_code)
                ev.delete()
                user = None
                try:
                    user = User.objects.get(username = mobile)
                    
                except:
                    pass
                if user is not None:
                    login(request , user)
                    return HttpResponseRedirect("/")
                
                else:
                    ru ,msg = register_user(request)
                    if ru:
                        return HttpResponseRedirect("/")
                    contex["error"] = msg
                
            else:
                contex["error"] = _('sms verification info not included')
                
        except Smsverificationcode.DoesNotExist:
            contex["error"] = _("verification code not found!")
            
    return render(request , "login.html",context=contex)  


          



def register_user(request):
    try:
        mobile = request.POST.get("mobile_number","")
        user = User.objects.create_user(mobile , None, random_password())
        user.save()
        if user is not None:
            login(request, user)
            return True, _("Welcome")
        else:
            return False, _("user not found")
                   
    except Exception:
        return False, _("user registrations failed")
    
    
def compare(request, product_id):
    pass