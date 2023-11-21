from django.contrib import admin
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from eshop.models import Category, Brand, PaymentMethod, ShippingMethod, Product, ProductImage, ProductProperty, \
    ProductMonetaryOption, Setting, Discount, Cart, CartItem, ShippingCost, PaymentStatus, DiscountCode, ShippingStatus, \
    Factor, FactorItem ,Smsverificationcode



@admin.register(Smsverificationcode)
class SmsverificationcodeAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["sms_verification_uuid", "mobile", "activation_code"]

    def get_list_display(self, request):
        return ["sms_verification_uuid", "mobile", "activation_code"]

    def get_search_fields(self, request):
        return ["sms_verification_uuid", "mobile", "activation_code"]


# from eshop.models import Publisher


# @admin.register(Publisher)
# class PublisherAdmin(admin.ModelAdmin):
#     def get_fields(self, request, obj=None):
#         return ["name", "address", "city", "country", "website"]
#
#     def get_list_display(self, request):
#         return ["name", "address", "website"]
#
#     def get_search_fields(self, request):
#         return ["name", "address", "website"]
#
#     def get_list_filter(self, request, filters=None):
#         return ["city", "country"]

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    def get_fields(self, request, obj=None):
        return ["title", "description", "parent"]

    def get_list_display(self, request):
        return ["title"]

    def get_search_fields(self, request):
        return ["title", "description"]

    # def get_list_filter(self, request, filters=None):
    #     return ["city", "country"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["title", "description"]

    def get_list_display(self, request):
        return ["title"]

    def get_search_fields(self, request):
        return ["title", "description"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["product", "percent", "is_active"]

    def get_list_display(self, request):
        return ["product", "percent", "is_active"]

    def get_search_fields(self, request):
        return ["product__title", "percent"]


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ["product", "count"]
    extra = 1


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):

    def get_fields(self, request, obj=None):
        fields = ("code", "percent",) + super().get_fields(request, obj)
        return fields

    def get_list_display(self, request):
        return ["code", "percent"]
    
        

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    inlines = [
        CartItemInline
    ]

    def get_fields(self, request, obj=None):
        fields = ("user",)
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            readonly_fields += ("user",)
        return readonly_fields

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display = (
            "user",
        ) + list_display
        return list_display


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["title", "code"]

    def get_list_display(self, request):
        return ["title", "code"]

    def get_search_fields(self, request):
        return ["title", "code"]


@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request)
        fields = ("code", "title",) + fields
        return (fields,)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request)
        if obj:
            return ("code",) + readonly_fields
        return readonly_fields

    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        search_fields = ("title",) + search_fields
        return search_fields

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display = (
            "title",
            "code"
        ) + list_display
        return list_display


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["title", "code", "payment_methods"]

    def get_list_display(self, request):
        return ["title", "code"]

    def get_search_fields(self, request):
        return ["title", "code"]


@admin.register(ShippingCost)
class ShippingCostAdmin(admin.ModelAdmin):

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request)
        fields = ["title", "states", "from_weight", "to_weight", "price", "description"] + fields
        return fields

    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        search_fields = ("title", "states", "from_weight", "to_weight", "price", "description",) + search_fields
        return search_fields

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display = (
            "title", "from_weight", "to_weight", "price",
        ) + list_display
        return list_display


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ["image"]
    extra = 1


class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    fields = ["title", "value"]
    extra = 1


class ProductMonetaryOptionInline(admin.TabularInline):
    model = ProductMonetaryOption
    fields = ["option", "price"]
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductPropertyInline, ProductMonetaryOptionInline]

    def get_fields(self, request, obj=None):
        return ["title", "category", "brand", "image", "description", "price", "view", "weight", "count", "shipping_methods", "is_featured", "min_purchase", "max_purchase", "has_value_added_tax", "is_active"]

    def get_list_display(self, request):
        return ["title", "image_tag", "category", "brand", "price", "view", "count", "is_active"]

    def get_search_fields(self, request):
        return ["title", "category", "brand", "description", "price", "view", "weight", "count", "min_purchase", "max_purchase",]

    def get_list_filter(self, request, filters=None):
        return ["category", "brand", "is_featured", "has_value_added_tax", "is_active"]


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):

    def get_fields(self, request, obj=None):
        return ["title", "site_title", "site_icon", "site_logo", "contact_us", "product_finishing_alert", "value_added_tax_percent"]

    def get_list_display(self, request):
        return ["title"]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(ShippingStatus)
class ShippingStatusAdmin(admin.ModelAdmin):

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request)
        fields = ("code", "title",) + fields
        return (fields,)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request)
        if obj:
            return ("code",) + readonly_fields
        return readonly_fields

    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        search_fields = ("title",) + search_fields
        return search_fields

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display = (
            "title",
            "code"
        ) + list_display
        return list_display

class FactorItemsInline(admin.TabularInline):
    model = FactorItem
    fields = ["product", "count"]
    extra = 1
    def has_delete_permission(self, request,obj= None):
        return False
    def has_add_permission(self, request, obj= None):
        return False
    def has_change_permission(self, request, obj= None):
        return False
 

@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    inlines = [FactorItemsInline]
    def print_button(self, obj):
        if obj:
            return mark_safe("<a class='btn btn-sm' style='background-color: #369; color: white;' href={}>چاپ فاکتور</a>"
                             .format(reverse("print_factor", kwargs={"factor_id": obj.uuid})))
    print_button.short_description = " "
    print_button.allow_tags = True


    def get_fields(self, request, obj=None):
        return ("uuid", "user", "price", "value_added_tax", "discount_code", "discount_price",
                "payment_method", "payment_status", "payment_tracking_code", "customer_comment",
                "shipping_method", "shipping_cost", "final_price", "shipping_status", "shipping_tracking_code",
                "name_family", "phone_number", "state", "city", "address", "post_code")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            if obj.payment_method.code == 1:
                readonly_fields += ("uuid", "user", "price", "value_added_tax", "discount_code", "discount_price",
                "payment_method", "payment_status", "payment_tracking_code", "customer_comment",
                "shipping_method", "shipping_cost", "final_price", "shipping_status", "shipping_tracking_code",
                "name_family", "phone_number", "state", "city", "address", "post_code")
            else:
                readonly_fields+= ("uuid", "user", "price", "value_added_tax", "discount_code", "discount_price",
                "payment_method", "payment_tracking_code", "customer_comment",
                "shipping_method", "shipping_cost", "final_price", "shipping_status", "shipping_tracking_code",
                "name_family", "phone_number", "state", "city", "address", "post_code")
        return readonly_fields

    def get_list_display(self, request):
        return ("uuid", "user", "payment_method", "payment_status", "final_price", "shipping_method", "shipping_status",
                "print_button")
