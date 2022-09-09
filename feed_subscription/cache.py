from django.core.cache import cache


def _get_user_channels_update_key(*args, user_id: int) -> str:
    return f"{user_id}-channels_update"


def _get_user_channel_update_key(*args, user_id: int, channel_id: int) -> str:
    return f"{user_id}-channels_update-{channel_id}"


def set_user_channels_updating(*args, user_id: int, insert: bool):
    key = _get_user_channels_update_key(user_id=user_id)
    if insert:
        cache.set(key=key, value="0")
    else:
        cache.delete(key)


def set_user_channel_updating(*args, user_id: int, channel_id: int, insert: bool):
    key = _get_user_channel_update_key(user_id=user_id, channel_id=channel_id)
    if insert:
        cache.set(key=key, value="0")
    else:
        cache.delete(key)


def is_user_channels_updating(*args, user_id: int) -> bool:
    key = _get_user_channels_update_key(user_id=user_id)
    result = cache.get(key)
    return result is not None


def is_user_channel_updating(*args, user_id: int, channel_id: int) -> bool:
    key = _get_user_channel_update_key(user_id=user_id, channel_id=channel_id)
    result = cache.get(key)
    return result is not None
