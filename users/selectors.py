from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from users.models import ApplicationUser


def user_exists_by_email(*args, email: str, update_user: Optional[ApplicationUser] = None) -> bool:
    q = ApplicationUser.objects.filter(email=email)
    if update_user is not None:
        q = q.exclude(id=update_user.id)
    return q.exists()


def get_user_by_id(*args, user_id: int) -> ApplicationUser:
    try:
        return ApplicationUser.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)
