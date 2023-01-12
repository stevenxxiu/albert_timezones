import json
from datetime import datetime
from pathlib import Path
from typing import Dict

import pytz
from albert import Action, Item, Query, QueryHandler, configLocation, setClipboardText  # pylint: disable=import-error


md_iid = '0.5'
md_version = '1.0'
md_name = 'Timezones'
md_description = 'Show times in a list of timezones.'
md_url = 'https://github.com/stevenxxiu/albert_timezones'
md_maintainers = '@stevenxxiu'
md_lib_dependencies = ['pytz']

TRIGGER = 'tz'
ICON_PATH = '/usr/share/icons/elementary/categories/64/preferences-system-time.svg'


class Plugin(QueryHandler):
    def __init__(self):
        super().__init__()
        # `{ readable_name: timezone_name }`
        self.timezones: Dict[str, pytz.timezone] = {}

    def id(self) -> str:
        return __name__

    def name(self) -> str:
        return md_name

    def description(self) -> str:
        return md_description

    def initialize(self) -> None:
        with (Path(configLocation()) / __name__ / 'settings.json').open() as sr:
            settings = json.load(sr)
            self.timezones = {
                readable_name: pytz.timezone(timezone_name) for readable_name, timezone_name in settings.items()
            }

    def defaultTrigger(self) -> str:
        return TRIGGER

    def handleQuery(self, query: Query) -> None:
        cur_time = datetime.now()
        fmt = '%Y/%m/%d %-I:%M:%S %p %z'

        for readable_name, timezone in self.timezones.items():
            dest_time_str = cur_time.astimezone(timezone).strftime(fmt).lower()
            copyable = f'{readable_name}: {dest_time_str}'

            query.add(
                Item(
                    id=f'{md_name}/{readable_name}',
                    text=dest_time_str,
                    subtext=readable_name,
                    icon=[ICON_PATH],
                    actions=[
                        Action(f'{md_name}/{readable_name}', 'Copy', lambda value_=copyable: setClipboardText(value_))
                    ],
                )
            )