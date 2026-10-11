#!/usr/bin/env python3
"""Start a plugin from the template.

    python3 tools/new_plugin.py bin_day                 # plugins/bin_day/, a plugin of this repository
    python3 tools/new_plugin.py bin_day ../my-plugin    # a folder of its own, for a repository of your own

It copies template/ and renames everything that carries the template's name: the component folder and files, the
C++ namespace and class (my_plugin -> bin_day, MyPlugin -> BinDay) and the manifest's id. The tile still counts days:
change it into yours (docs/MAKING_A_PLUGIN.md, "Step by step"), then run python3 tools/check.py <folder>. The check
fails until the template's maintainer (your-github-name), the LICENSE's "<year> <your name>" and the README's line that
it is the template are yours.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# AGENTS.md of a plugin in a repository of its own (CLAUDE.md beside it says to read it).
OWN_REPOSITORY = """# {id}: a plugin for Tessera

This repository is one plugin for Tessera, the ESP32 touch screens for Home Assistant. Its rules, its docs and its
tools live in the plugins repository: clone it beside this one, then read its AGENTS.md before you change anything.

```sh
git clone https://github.com/MaxGramser/tessera-plugins ../tessera-plugins
```

- The rules and the order to read the docs in: `../tessera-plugins/AGENTS.md`.
- Check the plugin, after every change: `python3 ../tessera-plugins/tools/check.py .` (must print `{id}: ok`).
- See what it draws on every kind of screen, after every change to its C++, its manifest or `preview.yaml`:
  `python3 ../tessera-plugins/tools/preview.py . --strict` (`--setup` once first; `../tessera-plugins/docs/PREVIEW.md`).
  The first build of each screen takes minutes. Read the findings it prints, `.preview/summary.json` and the pictures in
  `.preview/`, fix what it says, and run it again until it ends without a warning.
"""


def main():
    if len(sys.argv) < 2 or not re.fullmatch(r'[a-z][a-z0-9_]{0,31}', sys.argv[1]):
        raise SystemExit('usage: new_plugin.py <id> [folder]; an id is 1 to 32 of a-z, 0-9 and _, starting with a letter')
    plugin = sys.argv[1]
    target = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / 'plugins' / plugin
    if target.exists():
        raise SystemExit(f'{target} already exists')
    camel = ''.join(part.capitalize() for part in plugin.split('_'))
    shutil.copytree(ROOT / 'template', target)
    (target / 'components' / 'my_plugin').rename(target / 'components' / plugin)
    for path in sorted(target.rglob('*')):
        if path.is_file() and path.name.startswith('my_plugin'):
            path = path.rename(path.with_name(path.name.replace('my_plugin', plugin)))
        if path.is_file() and path.suffix in ('.py', '.h', '.cpp', '.yaml', '.md', '.json'):
            text = path.read_text(encoding='utf-8')
            text = text.replace('my_plugin', plugin).replace('MyPlugin', camel)
            path.write_text(text, encoding='utf-8')
    if ROOT / 'plugins' not in target.resolve().parents:
        # A repository of its own: whoever opens it, or their assistant, learns where the rules and the tools are.
        (target / 'AGENTS.md').write_text(OWN_REPOSITORY.format(id=plugin), encoding='utf-8')
        (target / 'CLAUDE.md').write_text('@AGENTS.md\n', encoding='utf-8')
    print(f'{target}: made from the template. Next: edit tessera-plugin.yaml (your GitHub name as maintainer), '
          f'translations/, components/{plugin}/, README.md (what your plugin does) and LICENSE (the year and your name; '
          f'a plugin in plugins/ of this repository may delete it), then python3 tools/check.py {target}')


if __name__ == '__main__':
    main()
