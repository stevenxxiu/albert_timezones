import json
from datetime import datetime
from pathlib import Path

import pytz
from albert import (
    Action,
    PluginInstance,
    StandardItem,
    TriggerQueryHandler,
    setClipboardText,
)

md_iid = '3.0'
md_version = '1.4'
md_name = 'Timezones'
md_description = 'Show times in a list of timezones'
md_license = 'MIT'
md_url = 'https://github.com/stevenxxiu/albert_timezones'
md_authors = ['@stevenxxiu']
md_lib_dependencies = ['pytz']

ICON_URL = f'file:{Path(__file__).parent / "icons/datetime.png"}'


class Plugin(PluginInstance, TriggerQueryHandler):
    def __init__(self):
        PluginInstance.__init__(self)
        TriggerQueryHandler.__init__(self)
        # `{ readable_name: timezone_name }`
        self.timezones: dict[str, pytz.tzinfo.BaseTzInfo] = {}

        with (self.configLocation() / 'settings.json').open() as sr:
            settings = json.load(sr)
            self.timezones = {
                readable_name: pytz.timezone(timezone_name) for readable_name, timezone_name in settings.items()
            }

    def defaultTrigger(self):
        return 'tz '

    def handleTriggerQuery(self, query) -> None:
        cur_time = datetime.now()
        fmt = '%Y/%m/%d %-I:%M:%S %p %z'

        for readable_name, timezone in self.timezones.items():
            dest_time_str = cur_time.astimezone(timezone).strftime(fmt).lower()
            copyable = f'{readable_name}: {dest_time_str}'

            query.add(
                StandardItem(
                    id=f'{md_name}/{readable_name}',
                    text=dest_time_str,
                    subtext=readable_name,
                    iconUrls=[ICON_URL],
                    actions=[
                        Action(f'{md_name}/{readable_name}', 'Copy', lambda value_=copyable: setClipboardText(value_))
                    ],
                )
            )
