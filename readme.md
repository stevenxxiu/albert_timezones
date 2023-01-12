# Albert Launcher Timezones Extension
## Install
To install, copy or symlink this directory to `~/.local/share/albert/org.albert.extension.python/modules/timezones/`.

## Config
Config is stored in `~/.config/albert/albert.timezones/settings.json`.

Example config:

```json
{
  "Melbourne": "Australia/Melbourne",
  "Netherlands": "Europe/Amsterdam"
}
```

## Development Setup
To setup the project for development, run:

    $ cd timezones/
    $ pre-commit install --hook-type pre-commit --hook-type commit-msg

To lint and format files, run:

    $ pre-commit run --all-files
