import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def password_validator(value):

    result = re.match("^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z]).{8,40}$", value)

    if result is None:
        raise ValidationError(_("Password should contains upper case, lower case letters and should be at least 8 characters long"))

    return value
