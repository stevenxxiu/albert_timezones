import json
from datetime import datetime
from pathlib import Path
from typing import Callable, override

import pytz
from albert import setClipboardText  # pyright: ignore[reportUnknownVariableType]
from albert import (
    Action,
    PluginInstance,
    Query,
    StandardItem,
    TriggerQueryHandler,
)

setClipboardText: Callable[[str], None]

md_iid = '3.0'
md_version = '1.4'
md_name = 'Timezones'
md_description = 'Show times in a list of timezones'
md_license = 'MIT'
md_url = 'https://github.com/stevenxxiu/albert_timezones'
md_authors = ['@stevenxxiu']
md_lib_dependencies = ['pytz']

ICON_URL = f'file:{Path(__file__).parent / "icons/datetime.png"}'


TimezonesSettings = dict[str, str]


class Plugin(PluginInstance, TriggerQueryHandler):
    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(self)
        # `{ readable_name: timezone_name }`
        self.timezones: dict[str, pytz.tzinfo.BaseTzInfo] = {}

        with (self.configLocation() / 'settings.json').open() as sr:
            settings: TimezonesSettings = json.load(sr)  # pyright: ignore[reportAny]
            self.timezones = {
                readable_name: pytz.timezone(timezone_name) for readable_name, timezone_name in settings.items()
            }

    @override
    def defaultTrigger(self):
        return 'tz '

    @override
    def handleTriggerQuery(self, query: Query) -> None:
        cur_time = datetime.now()
        fmt = '%Y/%m/%d %-I:%M:%S %p %z'

        for readable_name, timezone in self.timezones.items():
            dest_time_str = cur_time.astimezone(timezone).strftime(fmt).lower()
            copyable = f'{readable_name}: {dest_time_str}'

            copy_call: Callable[[str], None] = lambda value_=copyable: setClipboardText(value_)  # noqa: E731
            query.add(  # pyright: ignore[reportUnknownMemberType]
                StandardItem(
                    id=f'{md_name}/{readable_name}',
                    text=dest_time_str,
                    subtext=readable_name,
                    iconUrls=[ICON_URL],
                    actions=[Action(f'{md_name}/{readable_name}', 'Copy', copy_call)],
                )
            )
