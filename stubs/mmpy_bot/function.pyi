from _typeshed import Incomplete
from mmpy_bot.plugins import Plugin as Plugin
from mmpy_bot.utils import completed_future as completed_future
from mmpy_bot.webhook_server import NoResponse as NoResponse
from mmpy_bot.wrappers import Message as Message, WebHookEvent as WebHookEvent
from typing import Callable, TypeVar

log: Incomplete
ReturningType = TypeVar("ReturningType")


def listen_to(
    regexp: str,
    regexp_flag: int = ...,
    *,
    direct_only: bool = ...,
    needs_mention: bool = ...,
    allowed_users: Incomplete | None = ...,
    allowed_channels: Incomplete | None = ...,
    silence_fail_msg: bool = ...,
    **metadata: dict[Incomplete, Incomplete]
) -> Callable[[Callable[..., ReturningType]], ReturningType]: ...
