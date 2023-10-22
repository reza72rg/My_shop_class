import ast
import pytz

# from unidecode import unidecode
from django.template.defaultfilters import slugify
from datetime import datetime
from dateutil import parser
from django import template
from django.utils import timezone
from persiantools.jdatetime import JalaliDate
from django.conf import settings


register = template.Library()


persian_numbers = {
    "0":"۰",
    "1":"۱",
    "2":"۲",
    "3":"۳",
    "4":"۴",
    "5":"۵",
    "6":"۶",
    "7":"۷",
    "8":"۸",
    "9":"۹",
}


month_names_map = {
    "ژانویه": "01",
    "فوریه": "02",
    "مارس": "03",
    "آوریل": "04",
    "مه": "05",
    "ژوئن": "06",
    "ژوئیه": "07",
    "اوت": "08",
    "سپتامبر": "09",
    "اکتبر": "10",
    "نوامبر": "1",
    "دسامبر": "12",
}


def convert_to_persian_number(value):
    output = ""
    for v in value:
        try:
            output += persian_numbers[v]
        except Exception:
            output += v
    return output


def replace_date_string(date):
    day, month, year = date.split(" ")
    month = month_names_map[month]
    return "-".join([year, month, day])


@register.filter
def persian_date(value):
    return JalaliDate(value).strftime("%Y/%m/%d")


@register.simple_tag
def current_persian_year():
    return JalaliDate(datetime.now()).year


@register.filter
def persian_datetime_from_gregorian_farsi_datetime_str(value):
    try:
        if len(value) <= 4:
            return value
        date, time = value.split("،")
        date = replace_date_string(date)
        time_list = [t.zfill(2) for t in time.replace(" ساعت ", "").split(":")]
        time = ":".join(time_list)
        date_time = f"{date} {time}"
        return str(JalaliDate(timezone.localtime(parser.parse(date_time).replace(tzinfo=pytz.timezone(settings.TIME_ZONE))), locale='fa').strftime("%d %B %Y")) + " ساعت " + convert_to_persian_number(time)
    except Exception:
        return value


@register.filter
def eval(value):
    return ast.literal_eval(value)


@register.filter
def get_type(value):
    return type(value).__name__


@register.filter
def slug(value):
    return slugify(value)


@register.filter
def slugish(value):
    # return slugify(unidecode(value))
    return value.replace(" ", "-")
