import re
from re import Pattern
from typing import Callable, Dict, List, Tuple


class PluginManager:
    # don't import this directly -- import from bubbles.config
    def __init__(
        self, command_prefixes: Tuple, beginning_command_prefixes: Tuple
    ) -> None:
        self.plugins: List[Dict[str:Callable, str:Pattern, str:bool, str:str]] = list()
        self.callbacks: List[Callable] = list()
        self.command_prefixes = command_prefixes
        self.beginning_command_prefixes = beginning_command_prefixes

    def has_beginning_command_prefix(self, message: str) -> bool:
        return any(
            [
                message.lower().startswith(prefix)
                for prefix in self.beginning_command_prefixes
            ]
        )

    def has_command_prefix(self, message: str) -> bool:
        return any(
            [prefix.lower() in message.lower() for prefix in self.command_prefixes]
        )

    def message_is_for_us(self, message: str) -> bool:
        return any(
            [
                self.has_beginning_command_prefix(message),
                self.has_command_prefix(message),
            ]
        )

    def get_plugin(self, message: str) -> Callable:
        for plugin in self.plugins:
            if plugin["ignore_prefix"] or self.message_is_for_us(message):
                result = re.search(plugin["regex"], message)
                if result:
                    return plugin["callable"]

    def process_plugin_callbacks(self, data: Dict) -> None:
        for func in self.callbacks:
            func(data)

    def register_plugin(
        self,
        plugin: Callable,
        regex: str,
        flags=None,
        callback: Callable = None,
        ignore_prefix: bool = False,
        help: str = None,
    ) -> None:
        regex = re.compile(regex, flags if flags else 0)
        self.plugins.append(
            {
                "callable": plugin,
                "regex": regex,
                "ignore_prefix": ignore_prefix,
                "help": help,
            }
        )
        if callback:
            self.callbacks.append(callback)
        print(f"Registered {str(plugin)}")
