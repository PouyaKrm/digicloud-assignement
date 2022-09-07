from typing import Optional

from users.models import ApplicationUser


def user_exists_by_email(*args, email: str, update_user: Optional[ApplicationUser] = None) -> bool:
    q = ApplicationUser.objects.filter(email=email)
    if update_user is not None:
        q = q.exclude(id=update_user.id)
    return q.exists()

