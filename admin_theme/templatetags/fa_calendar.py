# -*- coding: utf-8 -*-
from datetime import date
from datetime import datetime

import pytz

from django import template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from main.calverter import Calverter

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


@register.filter
def data_number_format(input):
    return "/".join([input[:4], input[4:6], input[6:8]])


@register.filter
def to_persian_number(value):
    value = "".join([persian_digits.get(c, c) for c in value])
    return value


@register.filter
def gregorian_to_jalali(date, sep="-"):
    """
    Gets georgian date
    returns persian date in char(10) (/ separated)

    """
    if date == "" or date == None or date == "None":
        return ""
    date = "-".join("{0:0>2}".format(x) for x in str(date).split("-"))
    cal = Calverter()
    date_str = str(date)
    year = date_str[0:4]
    month = date_str[5:7]
    day = date_str[8:10]
    jd = cal.gregorian_to_jd(int(year), int(month), int(day))
    dat_tuple = cal.jd_to_jalali(jd, sep)
    return dat_tuple


#    format = "%s" + sep + "%s" + sep + "%s"
#    return format % (str(dat_tuple[0]).rjust(4, '0'), str(dat_tuple[1]).rjust(2, '0'), str(dat_tuple[2]).rjust(2, '0'))


@register.filter
def gregorian_to_jalali2(date, sep="/"):
    month_name = {
        1: "ژانویه",
        2: "فوریه",
        3: "مارس",
        4: "آوریل",
        5: "مه",
        6: "ژوئن",
        7: "ژوئیه",
        8: "اوت",
        9: "سپتامبر",
        10: "اکتبر",
        11: "نوامبر",
        12: "دسامبر",
    }
    if date == "" or date is None:
        return ""
    cal = Calverter()
    try:
        date = date.split("-")
    except:
        date = date.strftime("%m-%Y-%d")
        date = date.split("-")
    year = date[1]
    month = date[0]
    day = date[2]
    #     month_number = {v: k for k,v in month_name.items()}
    #     month = month_number[date[0]]
    jd = cal.gregorian_to_jd(int(year), int(month), int(day))
    dat_tuple = cal.jd_to_jalali(jd)
    return dat_tuple


@register.filter
def miladi_to_shamsi(value, sep="-"):
    # if get_language() == 'fa':
    return gregorian_to_jalali(value, sep)
    # else:
    #    return str(value)[:10]


@register.filter
def month_name_shamsi(month):
    month = int(month)
    farsi_month_name = {
        1: "فروردین",
        2: "اردیبهشت",
        3: "خرداد",
        4: "تیر",
        5: "مرداد",
        6: "شهریور",
        7: "مهر",
        8: "آبان",
        9: "آذر",
        10: "دی",
        11: "بهمن",
        12: "اسفند",
    }
    return "%s" % (farsi_month_name[month])


@register.filter
def miladi_to_shamsi2(value):
    jalali_date = gregorian_to_jalali2(value)
    year, month, day = jalali_date.split("/")
    year = int(year)
    month = int(month)
    day = int(day)
    farsi_month_name = {
        1: "فروردین",
        2: "اردیبهشت",
        3: "خرداد",
        4: "تیر",
        5: "مرداد",
        6: "شهریور",
        7: "مهر",
        8: "آبان",
        9: "آذر",
        10: "دی",
        11: "بهمن",
        12: "اسفند",
    }
    return "%s %s %s" % (day, farsi_month_name[month], year)


@register.filter
def miladi_to_shamsi_name_with_time(value):
    str_time = str(timezone.localtime(value.replace(tzinfo=pytz.timezone("Asia/Tehran"))).time().strftime("%H:%M:%S"))
    jalali_date = gregorian_to_jalali2(value)
    year, month, day = jalali_date.split("/")
    year = int(year)
    month = int(month)
    day = int(day)
    farsi_month_name = {
        1: "فروردین",
        2: "اردیبهشت",
        3: "خرداد",
        4: "تیر",
        5: "مرداد",
        6: "شهریور",
        7: "مهر",
        8: "آبان",
        9: "آذر",
        10: "دی",
        11: "بهمن",
        12: "اسفند",
    }
    return "%s %s %s - %s" % (day, farsi_month_name[month], year, str_time)


@register.filter
def miladi_to_shamsi3(value):
    if value:
        val = timezone.localtime(value.replace(tzinfo=pytz.timezone("Asia/Tehran")))
        return str(timezone.localtime(value).time().strftime("%H:%M:%S")) + " - " + gregorian_to_jalali(val, "/")
    else:
        return ""


@register.filter
def jalali_to_gregorian(dat_str, splitter="-"):
    """
    Gets date in (char(8)) (or / delimited) (or char(10) / delimited)
    returns Date
    returns None on error
    """
    cal = Calverter()
    try:
        year = None
        month = None
        day = None
        if len(dat_str) == 8:
            year = dat_str[0:4]
            month = dat_str[4:6]
            day = dat_str[6:8]
        elif len(dat_str) == 10:
            year = dat_str[0:4]
            month = dat_str[5:7]
            day = dat_str[8:10]
        else:
            splited = dat_str.split(splitter)
            year = splited[0]
            month = splited[1]
            day = splited[2]
        if not year.isdigit():
            return None
        if not month.isdigit():
            return None
        if not day.isdigit():
            return None
        jd = cal.jalali_to_jd(int(year), int(month), int(day))
        dat_tuple = cal.jd_to_gregorian(jd)
        return date(dat_tuple[0], dat_tuple[1], dat_tuple[2])
    except Exception:
        # print msg
        return None


# by kasaiee


@register.filter
def jd_to_jalali_by_char(gregorian):
    # converting gregorian date type to str from any other types
    if type(gregorian) is not str:
        gregorian = str(gregorian)
    gr = gregorian.split("-")
    cal = Calverter()
    gr = [int(i) for i in gr]
    jd = cal.gregorian_to_jd(gr[0], gr[1], gr[2])  # year month day
    jalali = cal.jd_to_jalali(jd)
    MONTH_NAME = {
        "01": _("Farvardin"),  # _('January'),
        "02": _("Ordibehesht"),  # _('January'),
        "03": _("Khordad"),  # _('March'),
        "04": _("Tir"),  # _('April'),
        "05": _("Mordad"),  # _('May'),
        "06": _("Shahrivar"),  # _('June'),
        "07": _("Mehr"),  # _('July'),
        "08": _("Aban"),  # _('August'),
        "09": _("Azar"),  # _('September'),
        "10": _("Dey"),  # _('October'),
        "11": _("Bahman"),  # _('November'),
        "12": _("Esfand"),  # _('December')
    }
    jl = [str(i) for i in jalali.split("/")]
    jalali = [
        jl[0],
        MONTH_NAME.get(jl[1]).__str__(),
        jl[2],
    ]
    return " ".join(jalali)


# @register.filter
# def jalali_today():
#     date = datetime.now().date()
#     return Calverter().gregorgian_to_jalali(date)


# *************************************************************************************** #


@register.filter
def jalali_by_weekday(date_obj):
    date = gregorian_to_jalali(str(timezone.localtime(date_obj)), sep="-")
    weekday = timezone.localtime(date_obj).strftime("%w")
    year, month, day = date.split("-")
    month = int(month)
    MONTH_NAME = {
        1: "فروردین",
        2: "اردیبهشت",
        3: "خرداد",
        4: "تیر",
        5: "مرداد",
        6: "شهریور",
        7: "مهر",
        8: "آبان",
        9: "آذر",
        10: "دی",
        11: "بهمن",
        12: "اسفند",
    }
    DAY_NAME = {
        "0": "یکشنبه",  # Sunday
        "1": "دوشنبه",  # 'Monday'
        "2": "سه شنبه",  # 'Tuesday'
        "3": "چهارشنبه",  # 'Wednesday'
        "4": "پنجشنبه",  # 'Thursday'
        "5": "جمعه",  # 'Friday'
        "6": "شنبه",  # 'Saturday'
    }

    if int(day) < 10:
        day = day[1]
    return "%s - %s %s %s" % (DAY_NAME.get(weekday), to_persian_number(day), MONTH_NAME[month], to_persian_number(year))


@register.filter
def persian_datetime(date_obj):
    pass


@register.filter
def jalali_by_weekday_and_time(date_obj):
    date = gregorian_to_jalali(str(timezone.localtime(date_obj)), sep="-")
    weekday = timezone.localtime(date_obj).strftime("%w")
    year, month, day = date.split("-")
    month = int(month)
    time = timezone.localtime(date_obj)

    MONTH_NAME = {
        1: "فروردین",
        2: "اردیبهشت",
        3: "خرداد",
        4: "تیر",
        5: "مرداد",
        6: "شهریور",
        7: "مهر",
        8: "آبان",
        9: "آذر",
        10: "دی",
        11: "بهمن",
        12: "اسفند",
    }
    DAY_NAME = {
        "0": "یکشنبه",  # Sunday
        "1": "دوشنبه",  # 'Monday'
        "2": "سه شنبه",  # 'Tuesday'
        "3": "چهارشنبه",  # 'Wednesday'
        "4": "پنجشنبه",  # 'Thursday'
        "5": "جمعه",  # 'Friday'
        "6": "شنبه",  # 'Saturday'
    }

    if int(day) < 10:
        day = day[1]
    return to_persian_number(
        "%s - %s %s %s - %s"
        % (
            DAY_NAME.get(weekday),
            to_persian_number(day),
            MONTH_NAME[month],
            to_persian_number(year),
            time.strftime("%H:%M:%S"),
        )
    )


@register.filter
def gregorian_by_weekday(date_obj):
    date = str(date_obj.date())
    weekday = date_obj.strftime("%w")
    year, month, day = date.split("-")
    month = int(month)
    MONTH_NAME = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }
    DAY_NAME = {
        "0": "Sunday",
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5": "Friday",
        "6": "Saturday",
    }

    return "%s - %s %s %s" % (DAY_NAME.get(weekday), day, MONTH_NAME[month], year)


@register.filter
def gregorian_to_hijri(date):
    cal = Calverter()
    year, month, day = date.split("-")
    jd = cal.gregorian_to_jd(year, month, day)
    islamic_today = cal.jd_to_islamic(jd)
    return islamic_today


@register.filter
def hijri_by_weekday(date_obj, sep="-"):
    date_str = str(date_obj.date())
    weekday = date_obj.strftime("%w")
    date = gregorian_to_hijri(date_str)
    month = int(date[1])
    MONTH_NAME = {
        1: "محرم",  # _('moharam'),
        2: "صفر",  # _('safar'),
        3: "ربيع الاول",  # _('rabiolaval'),
        4: "ربيع الثاني",  # _('rabiolakhar'),
        5: "جمادي الاول",  # _('jamadiolavl'),
        6: "جمادي الثاني",  # _('jamadiolsani'),
        7: "رجب",  # _('rajab'),
        8: "شعبان",  # _('shaban'),
        9: "رمضان",  # ('ramezan'),
        10: "شوال",  # _('sheval'),
        11: "ذیقعده",  # _('zighade'),
        12: "ذالحجه",  # _('zihaje'),
    }
    DAY_NAME = {
        "0": "الاحد",  # _('al-ahad'), u'یکشنبه',
        "1": "الإثنين",  # _("al-'ithnayn"), u'دوشنبه',
        "2": "الثلاثاء",  # _("ath-thalatha'"), u'سه شنبه',
        "3": "الاربعاء",  # _("al-arbia`aa'"), u'چهارشنبه',
        "4": "الخميس",  # _("al-khamis"), u'پنجشنبه',
        "5": "الجمعة",  # _("al-jumu`a"), u'جمعه',
        "6": "السبت",  # _("as-sabt"), u'شنبه',
    }
    return "%s - %s %s %s" % (DAY_NAME.get(weekday), date[2], MONTH_NAME[month], date[0])


@register.filter
def gregorian_to_jalali_by_time(date_obj):
    date = jalali_by_weekday(date_obj)
    time = date_obj.now().strftime("%H:%M")
    return "%s ساعت %s" % (date, to_persian_number(time))


@register.filter
def jalali_by_month_name(date_obj):
    if date_obj == "" or date_obj == None or date_obj == "None":
        return ""
    if not isinstance(date_obj, str):
        date_obj = str(date_obj)
    date = miladi_to_shamsi(date_obj)
    year, month, day = date.split("-")
    month = int(month)
    MONTH_NAME = {
        1: _("Farvardin"),  # u'فروردین',
        2: _("Ordibehesht"),  # u'اردیبهشت',
        3: _("Khordad"),  # u'خرداد',
        4: _("Tir"),  # u'تیر',
        5: _("Mordad"),  # u'مرداد',
        6: _("Shahrivar"),  # u'شهریور',
        7: _("Mehr"),  # u'مهر',
        8: _("Aban"),  # u'آبان',
        9: _("Azar"),  # u'آذر',
        10: _("Dey"),  # u'دی',
        11: _("Bahman"),  # u'بهمن',
        12: _("Esfand"),  # u'اسفند',
    }

    if int(day) < 10:
        day = day[1]

    return "%s %s %s" % (to_persian_number(day), MONTH_NAME[month], to_persian_number(year))


@register.filter
def shamsi_month_start_end(date_obj=None):
    d = date_obj
    if date_obj is None:
        d = datetime.now()
    timezone = pytz.timezone("Asia/Tehran")
    d_aware = timezone.localize(d)
    sh_date = miladi_to_shamsi3(d_aware)
    year, month, _ = sh_date.rpartition("-")[2].strip().split("/")

    start_year = year
    end_year = year
    start_month = month
    end_month = month

    if int(month) == 12:
        end_year = int(year) + 1
        end_month = "01"
    else:
        end_month = "{0:02}".format(int(end_month) + 1)

    start_date = f"{start_year}/{start_month}/01"
    end_date = f"{end_year}/{end_month}/01"

    sd = jalali_to_gregorian(start_date)
    ed = jalali_to_gregorian(end_date)
    start_date = datetime(sd.year, sd.month, sd.day)
    end_date = datetime(ed.year, ed.month, ed.day)

    start_date = timezone.localize(start_date)
    end_date = timezone.localize(end_date)

    return start_date, end_date
