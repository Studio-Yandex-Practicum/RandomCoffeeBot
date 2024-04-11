from abc import ABC
from typing import Any, Callable, Generic, Protocol, TypeVar

from _typeshed import Incomplete
from mmpy_bot.plugins import Plugin as Plugin
from mmpy_bot.utils import completed_future as completed_future
from mmpy_bot.webhook_server import NoResponse as NoResponse
from mmpy_bot.wrappers import Message as Message
from mmpy_bot.wrappers import WebHookEvent as WebHookEvent

log: Incomplete
ReturningType = TypeVar("ReturningType", covariant=True)

class MessageFunction(Protocol, Generic[ReturningType]):
    async def __call__(self_, self: Plugin, message: Message, *args) -> ReturningType: ...  # type: ignore

def listen_to(
    regexp: str,
    regexp_flag: int = 0,
    *,
    direct_only: bool = False,
    needs_mention: bool = False,
    allowed_users: Any = None,
    allowed_channels: Any = None,
    silence_fail_msg: Any = False,
    **metadata: dict[str, Any],
) -> Callable[[Callable[..., ReturningType]], MessageFunction[ReturningType]]:
    """Wrap the given function in a MessageFunction class so we can register some
    properties."""

def listen_webhook(
    regexp: str, **metadata: dict[Incomplete, Incomplete]
) -> Callable[[Callable[..., ReturningType]], Callable[..., ReturningType]]: ...

class Function(ABC): ...
class WebHookFunction(Function): ...
