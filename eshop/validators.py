import datetime
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_postcode(value):
    try:
        int(value)
        if len(value) != 10:
            raise ValueError
        if value[0] == "0":
            raise ValueError
    except (ValueError, TypeError):
        raise ValidationError(_("Enter a valid postcode"), code="invalid")


def validate_mobile(value):
    try:
        int(value)
        if len(value) != 11:
            raise ValueError
        if value[0:2] == "09":
            raise ValueError
    except (ValueError, TypeError):
        raise ValidationError(_("Enter a valid mobile number"), code="invalid")


def validate_birth_date(value, age=18):
    try:
        if value > (datetime.datetime.today() - datetime.timedelta(days=age*365)).date():
            raise ValueError
    except (ValueError, TypeError):
        raise ValidationError(_("Enter a valid birth date"), code="invalid")


def _check_melli_code(value):
    if not re.search(r"^\d{10}$", value):
        return False

    check = int(value[9])
    s = sum(map(lambda x: int(value[x]) * (10 - x), range(0, 9))) % 11
    return s < 2 and check == s or s >= 2 and check + s == 11


def validate_melli_code(value):
    try:
        int(value)
        if len(value) != 10:
            raise ValueError
        if not _check_melli_code(value):
            raise ValueError
    except (ValueError, TypeError):
        raise ValidationError(_("Enter a valid melli code"), code="invalid")
