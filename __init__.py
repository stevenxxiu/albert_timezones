import json
from collections.abc import Generator
from datetime import datetime
from pathlib import Path
from typing import Callable, override
from zoneinfo import ZoneInfo

from albert import setClipboardText  # pyright: ignore[reportUnknownVariableType]
from albert import (
    Action,
    GeneratorQueryHandler,
    Icon,
    Item,
    PluginInstance,
    QueryContext,
    StandardItem,
)

setClipboardText: Callable[[str], None]

md_iid = '5.0'
md_version = '1.5'
md_name = 'Timezones'
md_description = 'Show times in a list of timezones'
md_license = 'MIT'
md_url = 'https://github.com/stevenxxiu/albert_timezones'
md_authors = ['@stevenxxiu']

ICON_PATH = Path(__file__).parent / 'icons/datetime.png'


TimezonesSettings = dict[str, str]


class Plugin(PluginInstance, GeneratorQueryHandler):
    def __init__(self) -> None:
        PluginInstance.__init__(self)
        GeneratorQueryHandler.__init__(self)
        # `{ readable_name: timezone }`
        self.timezones: dict[str, ZoneInfo] = {}

        with (self.configLocation() / 'settings.json').open() as sr:
            settings: TimezonesSettings = json.load(sr)  # pyright: ignore[reportAny]
            self.timezones = {
                readable_name: ZoneInfo(timezone_name) for readable_name, timezone_name in settings.items()
            }

    @override
    def defaultTrigger(self) -> str:
        return 'tz '

    @override
    def items(self, ctx: QueryContext) -> Generator[list[Item]]:
        cur_time = datetime.now()
        fmt = '%Y/%m/%d %-I:%M:%S %p %z'

        items: list[Item] = []
        for readable_name, timezone in self.timezones.items():
            dest_time_str = cur_time.astimezone(timezone).strftime(fmt).lower()
            copyable = f'{readable_name}: {dest_time_str}'

            copy_call: Callable[[str], None] = lambda value_=copyable: setClipboardText(value_)  # noqa: E731
            item = StandardItem(
                id=readable_name,
                text=dest_time_str,
                subtext=readable_name,
                icon_factory=lambda: Icon.image(ICON_PATH),
                actions=[Action('copy', 'Copy', copy_call)],
            )
            items.append(item)
        yield items
