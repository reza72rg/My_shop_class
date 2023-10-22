from PIL import Image
from io import BytesIO

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _
from django.db.models.fields.files import ImageFieldFile
from django.core.files import File
from mptt.models import MPTTModel, TreeForeignKey

from admin_theme.models import State
from admin_theme.tools import create_code
from main.tools import UploadToPathAndRename
from django.utils.safestring import mark_safe
from django.conf import settings
from ckeditor.fields import RichTextField


def get_image_field(self):
    output = []
    for k, v in self.__dict__.items():
        if isinstance(v, ImageFieldFile):
            output.append(k)
    return output


class MainModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name=_("create date"))
    modify_date = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name=_("modify date"))
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))

    def save(self, *args, **kwargs):
        image_fields = get_image_field(self)
        if image_fields:
            for i in image_fields:
                if hasattr(self, i) and isinstance(getattr(self, i), ImageFieldFile):
                    image = Image.open(getattr(self, i).file)
                    image_io = BytesIO()
                    image_extension = getattr(self, i).name.rpartition(".")[-1].upper()
                    image_extension = "JPEG" if image_extension == "JPG" else image_extension
                    image.save(image_io, image_extension, quality=60)
                    new_image = File(image_io, name=getattr(self, i).name)
                    setattr(self, i, new_image)
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


# class Category(models.Model):
#     title = models.CharField(max_length=200, verbose_name=_("title"))
#     description = models.TextField(default="",  verbose_name=_("description"), blank=True, null=True)
#
#     def __unicode__(self):
#         return self.title
#
#     def __str__(self):
#         return self.title
#
#     class Meta:
#         verbose_name = _("category")
#         verbose_name_plural = _("categories")


class Category(MPTTModel):
    order = models.PositiveSmallIntegerField(default=0, verbose_name=_("order"))
    title = models.CharField(max_length=200, verbose_name=_("title"))
    description = models.TextField(default="",  verbose_name=_("description"), blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Brand(MainModel):
    title = models.CharField(max_length=200, verbose_name=_("title"))

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")


class PaymentMethod(MainModel):
    code = models.PositiveSmallIntegerField(default=0, verbose_name=_("code"), unique=True)
    title = models.CharField(max_length=200, verbose_name=_("title"))

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("paymwent method")
        verbose_name_plural = _("payment methods")


class ShippingMethod(MainModel):
    code = models.PositiveSmallIntegerField(default=0, verbose_name=_("code"), unique=True)
    title = models.CharField(max_length=200, verbose_name=_("title"))
    payment_methods = models.ManyToManyField(PaymentMethod, verbose_name=_("payment methods"))

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("shipping method")
        verbose_name_plural = _("shipping methods")


class ShippingCost(MainModel):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    states = models.ManyToManyField(State, verbose_name=_("destination states"))
    from_weight = models.PositiveIntegerField(default=0, verbose_name=_("from weight"), help_text=_("Grams"))
    to_weight = models.PositiveIntegerField(default=0, verbose_name=_("to weight"), help_text=_("Grams"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("price"), help_text="toman")
    description = models.TextField(default='', blank=True, null=True, verbose_name=_("description"))

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _("shipping cost")
        verbose_name_plural = _("shipping costs")


class Product(MainModel):
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, verbose_name=_("brand"), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name=_("title"))
    image = models.ImageField(verbose_name=_("product image"), upload_to=UploadToPathAndRename("products"))
    image_cropping_info = models.CharField(verbose_name="cropping info", max_length=100, blank=True, null=True)
    description = models.TextField(default="",  verbose_name=_("description"), blank=True, null=True)
    view = models.PositiveIntegerField(default=0, verbose_name=_("view"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("price"))
    release_date = models.DateTimeField(_("release date"), blank=True, null=True)
    weight = models.PositiveIntegerField(default=0, verbose_name=_("weight"), help_text=_("input value as Grams"))
    count = models.PositiveIntegerField(default=100, verbose_name=_("count"))
    shipping_methods = models.ManyToManyField(ShippingMethod, verbose_name=_("shipping merthods"))
    is_featured = models.BooleanField(default=False, verbose_name=_("is featured"))
    min_purchase = models.PositiveIntegerField(default=0, verbose_name=_("minimum purchase"))
    max_purchase = models.PositiveIntegerField(default=100, verbose_name=_("maximum purchase"))
    has_tax = models.BooleanField(default=False, verbose_name=_("has tax"))
    tax_percent = models.PositiveIntegerField(default=0, verbose_name=_("tax percent"), validators=[MaxValueValidator(100)])
    has_value_added_tax = models.BooleanField(default=False, verbose_name=_("has value added tax"))
    meta_keywords = models.CharField(verbose_name=_("keywords"), help_text=_("separate with comma (used in the site's header for seo)"), max_length=200, blank=True, null=True)

    def image_tag(self):
        return mark_safe(f'<img src="{settings.MEDIA_URL}{self.image}" height="50" />')
    image_tag.allow_tags = True
    image_tag.short_description = "---"

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        unique_together = [["title", "category"], ["title", "brand"]]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_("product image"), upload_to=UploadToPathAndRename("products"))

    def __unicode__(self):
        return str(self.product.title)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class ProductProperty(MainModel):
    """set product property fields"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("product"))
    title = models.CharField(default='', max_length=255, verbose_name=_("title"))
    value = models.CharField(default='', max_length=255, verbose_name=_("value"))

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)

    class Meta:
        """product property meta"""
        verbose_name = _("product property")
        verbose_name_plural = _("product properties")


class ProductMonetaryOption(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    option = models.CharField(max_length=200, verbose_name=_("option"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("price"), help_text="Toman")

    def __unicode__(self):
        return self.product.title

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _("product monetary option")
        verbose_name_plural = _("product monetary options")


class Discount(MainModel):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name=_("product"))
    percent = models.PositiveIntegerField(default=0, verbose_name=_("discount percent"), validators=[MaxValueValidator(100), MinValueValidator(1)])

    class Meta:
        verbose_name = _("discount")
        verbose_name_plural = _("discounts")

    def __unicode__(self):
        return f"{str(self.product)} - {str(self.percent)}"

    def __str__(self):
        return f"{str(self.product)} - {str(self.percent)}"


class DiscountCode(MainModel):
    """set discount code fields"""
    percent = models.PositiveIntegerField(default=0, verbose_name=_("discount percent"), validators=[MaxValueValidator(100), MinValueValidator(1)])
    code = models.CharField(max_length=255, unique=True, default=create_code, verbose_name=_("code"))

    class Meta:
        """discount code meta"""
        verbose_name = _("discount code")
        verbose_name_plural = _("discount codes")

    def __unicode__(self):
        return str(self.code) + " - " + str(self.percent)

    def __str__(self):
        return str(self.code) + " - " + str(self.percent)


class Cart(MainModel):
    """set cart fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, verbose_name=_("discount code"), blank=True, null=True)

    class Meta:
        """cart meta"""
        verbose_name = _("cart")
        verbose_name_plural = _("carts")

    def __unicode__(self):
        return str(self.user)

    def __str__(self):
        return str(self.user)


class CartItem(MainModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_("cart"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("product"))
    monetary_option = models.ForeignKey(ProductMonetaryOption, on_delete=models.CASCADE, verbose_name=_("monetary option"), null=True, blank=True)
    count = models.PositiveIntegerField(default=1, verbose_name=_("count"), validators=[MinValueValidator(1)])
    price = models.PositiveIntegerField(default=0, verbose_name=_("price"))

    class Meta:
        verbose_name = _("cart item")
        verbose_name_plural = _("cart items")

    def __unicode__(self):
        return f"{str(self.cart)} - {self.product} - {self.count}"

    def __str__(self):
        return f"{str(self.cart)} - {self.product} - {self.count}"


class ShippingStatus(MainModel):
    """set shipping status fields"""
    code = models.PositiveSmallIntegerField(default=0, verbose_name=_("code"), unique=True)
    title = models.CharField(max_length=255, unique=True, default="", verbose_name=_("title"))

    class Meta:
        """shipping status meta"""
        ordering = ("code",)
        verbose_name = _("shipping status")
        verbose_name_plural = _("shipping statuses")

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)


class PaymentStatus(MainModel):
    """set payment status fields"""
    code = models.PositiveSmallIntegerField(default=0, verbose_name=_("code"), unique=True)
    title = models.CharField(max_length=255, unique=True, default="", verbose_name=_("title"))

    class Meta:
        """payment status meta"""
        ordering = ("code",)
        verbose_name = _("payment status")
        verbose_name_plural = _("payment statuses")

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)


class Setting(MainModel):
    title = models.CharField(max_length=200, verbose_name=_("title"), blank=True, null=True)
    site_title = models.CharField(max_length=200, verbose_name=_("site title"), blank=True, null=True)
    site_icon = models.ImageField(verbose_name=_("site icon"), upload_to=UploadToPathAndRename("setting"))
    site_logo = models.ImageField(verbose_name=_("site logo"), upload_to=UploadToPathAndRename("setting"))
    contact_us = RichTextField()
    product_finishing_alert = models.PositiveIntegerField(default=10, verbose_name=_("product finishing alert"))
    value_added_tax_percent = models.PositiveIntegerField(default=9, verbose_name=_("value added tax percent"), validators=[MaxValueValidator(100), MinValueValidator(1)])
    has_value_added_tax = models.BooleanField(default=True, verbose_name=_("has value added tax"))
    soomasoft_webservice_user = models.CharField(default='', max_length=50, verbose_name=_("soomasoft web service user"))
    soomasoft_webservice_password = models.CharField(default='', max_length=50, verbose_name=_("soomasoft web service password"))
    soomasoft_webservice_otp_number = models.CharField(default='', max_length=50, verbose_name=_("soomasoft otp number"))
    class Meta:
        verbose_name = _("settings")
        verbose_name_plural = _("settings")

    def __unicode__(self):
        return str(self.title)

    def __str__(self):
        return str(self.title)
