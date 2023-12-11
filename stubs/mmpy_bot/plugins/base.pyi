import re
from abc import ABC
from typing import Any, Dict, List, Optional, Sequence, Union

from _typeshed import Incomplete
from mmpy_bot.driver import Driver as Driver
from mmpy_bot.function import Function as Function
from mmpy_bot.function import MessageFunction as MessageFunction
from mmpy_bot.function import WebHookFunction as WebHookFunction
from mmpy_bot.settings import Settings as Settings
from mmpy_bot.utils import split_docstring as split_docstring
from mmpy_bot.wrappers import EventWrapper as EventWrapper

log: Incomplete

class Plugin(ABC):
    driver: Incomplete
    plugin_manager: Incomplete
    settings: Incomplete
    docstring: Incomplete
    def __init__(self) -> None: ...
    def initialize(self, driver: Driver, plugin_manager: PluginManager, settings: Settings) -> None: ...
    def on_start(self) -> None: ...
    def on_stop(self) -> Plugin: ...
    async def call_function(
        self, function: Function, event: EventWrapper, groups: Optional[Sequence[str]] = ...
    ) -> None: ...

class FunctionInfo:
    help_type: str
    location: str
    function: Function
    pattern: str
    docheader: str
    docfull: str
    direct: bool
    mention: bool
    is_click: bool
    metadata: dict[Incomplete, Incomplete]
    def __init__(
        self,
        help_type: str,
        location: str,
        function: Function,
        pattern: str,
        docheader: str,
        docfull: str,
        direct: bool,
        mention: bool,
        is_click: bool,
        metadata: dict[Incomplete, Incomplete],
    ) -> None: ...

def get_function_characteristics(function: FunctionInfo) -> tuple[bool, bool, str]: ...
def generate_plugin_help(
    listeners: Dict[re.Pattern[Any], List[Union[MessageFunction[Any], WebHookFunction]]]
) -> list[FunctionInfo]: ...

class PluginManager:
    settings: Incomplete
    plugins: Incomplete
    message_listeners: Incomplete
    webhook_listeners: Incomplete
    def __init__(self, plugins: Sequence[Plugin]) -> None: ...
    def initialize(self, driver: Driver, settings: Settings) -> None: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    def get_help(self) -> List[FunctionInfo]: ...
