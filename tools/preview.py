#!/usr/bin/env python3
"""The plugin bench: see your plugin on every kind of screen, on the screens' real firmware, built for your computer.

    python3 tools/preview.py --setup                    # once: checks SDL2 and a compiler, makes its own Python
    python3 tools/preview.py plugins/my_idea            # the default screens: small, middle, standing up, large
    cd plugins/my_idea && python3 ../../tools/preview.py  # the plugin of the folder you are in
    python3 tools/preview.py plugins/my_idea --all      # every board Tessera has, lying down and standing up
    python3 tools/preview.py plugins/my_idea --screen 1024x600@7 --grid max
    python3 tools/preview.py plugins/my_idea --board guition --window --watch

It reads what your plugin adds (its manifest and its code: the tiles and their sizes, cards, top bar items, settings
rows, questions to Home Assistant), builds each screen with it, gives its tiles the data of your preview.yaml as the
Tessera app would, and photographs everything: every tile at every size, light and dark, every card, the top bar, the
settings page. It checks what it draws and writes <plugin>/.preview/index.html. docs/PREVIEW.md says it all.

The bench (tools/bench.py) builds on a copy of Tessera, so what it shows is the firmware's own code: this tool keeps
one in tools/.cache/tessera-main, the firmware every screen runs (TESSERA_REF=dev for what comes next, and a plugin
whose manifest names an API newer than main's gets dev by itself; TESSERA_TREE a checkout of your own), and a Python
with ESPHome in tools/.cache/preview-venv.
"""
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'tools' / '.cache'
VENV = CACHE / 'preview-venv'
REPOSITORY = 'https://github.com/MaxGramser/homeassistant_espscreen'
# The firmware the bench builds: main, what every screen runs, unless TESSERA_REF names another branch.
REF = os.environ.get('TESSERA_REF', 'main')
FRESH = 3600   # the copy of Tessera is fetched again when it is an hour old
BENCH = ROOT / 'tools' / 'bench.py'
# What the bench builds on in Tessera: its host build and render harness.
HARNESS = Path('tools') / 'render' / 'host.py'


def say(text):
    print(text, flush=True)


def stop(text):
    raise SystemExit(f'preview: {text}')


def run(command, **kw):
    return subprocess.run(command, check=True, **kw)


def core(ref=None):
    """Tessera's repository: TESSERA_TREE, or a shallow copy of a branch of it (main unless told otherwise), fetched
    again when it is an hour old. Each branch has a copy of its own (tools/.cache/tessera-<branch>)."""
    own = os.environ.get('TESSERA_TREE')
    if own:
        tree = Path(own).expanduser().resolve()
        if not (tree / HARNESS).is_file():
            stop(f'TESSERA_TREE={tree} has no {HARNESS}: a checkout of Tessera')
        return tree
    ref = ref or REF
    if not shutil.which('git'):
        stop('git is needed to fetch Tessera; install it (macOS: xcode-select --install, Linux: apt install git)')
    copy = CACHE / f'tessera-{ref}'
    stamp = copy / '.git' / 'FETCH_HEAD'
    if not (copy / '.git').is_dir():
        say(f'Fetching the firmware: Tessera\'s {ref} into {copy} ...')
        CACHE.mkdir(parents=True, exist_ok=True)
        run(['git', 'clone', '--quiet', '--depth', '1', '--branch', ref, REPOSITORY, str(copy)])
    elif not stamp.exists() or time.time() - stamp.stat().st_mtime > FRESH:
        say(f'Updating the firmware: Tessera\'s {ref} ...')
        try:
            run(['git', '-C', str(copy), 'fetch', '--quiet', '--depth', '1', 'origin', ref])
            run(['git', '-C', str(copy), 'reset', '--quiet', '--hard', 'FETCH_HEAD'])
        except subprocess.CalledProcessError:
            say('  could not reach GitHub: using the copy there is')
    if not (copy / HARNESS).is_file():
        stop(f'Tessera\'s {ref} has no host build ({HARNESS})')
    return copy


def offered(tree):
    """The plugin API a copy of Tessera offers (plugin_manifest.PLUGIN_API)."""
    found = re.search(r'PLUGIN_API = \((\d+), (\d+)\)', (tree / 'screen_manager' / 'app' / 'plugin_manifest.py').read_text())
    return (int(found[1]), int(found[2])) if found else (0, 0)


def wanted(folder):
    """The plugin API a manifest names, as (major, minor)."""
    found = re.search(r'(?m)^api:\s*["\']?(\d+)\.(\d+)', (folder / 'tessera-plugin.yaml').read_text(encoding='utf-8'))
    return (int(found[1]), int(found[2])) if found else (0, 0)


def esphome_version(tree):
    """The ESPHome the Tessera app builds screens with (its Dockerfile), so the bench builds what a screen runs."""
    found = re.search(r'esphome/esphome:(\d{4}\.\d+\.\d+)', (tree / 'screen_manager' / 'Dockerfile').read_text())
    if not found:
        stop('the ESPHome version of Tessera\'s Dockerfile cannot be read')
    return found[1]


def python_of_venv():
    return VENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')


def esphome_of_venv():
    return VENV / ('Scripts/esphome.exe' if os.name == 'nt' else 'bin/esphome')


def hints():
    """What to install for this system, as commands to paste."""
    system = platform.system()
    if system == 'Darwin':
        return {'sdl2': 'brew install sdl2   (Homebrew: https://brew.sh)', 'compiler': 'xcode-select --install',
                'python': 'brew install python@3.13'}
    if system == 'Linux':
        return {'sdl2': 'sudo apt install libsdl2-dev   (Fedora: sudo dnf install SDL2-devel)',
                'compiler': 'sudo apt install build-essential   (Fedora: sudo dnf install gcc-c++ make)',
                'python': 'sudo apt install python3 python3-venv'}
    return {'sdl2': 'use WSL 2 (Ubuntu) and run the bench there', 'compiler': 'use WSL 2 (Ubuntu)', 'python': 'use WSL 2 (Ubuntu)'}


def missing():
    """What this computer lacks for the bench: [(what, how to get it)]."""
    how, out = hints(), []
    if platform.system() not in ('Darwin', 'Linux'):
        return [('a Mac or Linux (on Windows: WSL 2)', how['sdl2'])]
    if sys.version_info < (3, 11) and not shutil.which('uv') and interpreter() == sys.executable:
        out.append((f'Python 3.11 or newer (this is {platform.python_version()})', how['python']))
    if not (shutil.which('c++') or shutil.which('g++') or shutil.which('clang++')):
        out.append(('a C++ compiler', how['compiler']))
    sdl = shutil.which('sdl2-config') or (shutil.which('pkg-config') and subprocess.run(
        ['pkg-config', '--exists', 'sdl2'], capture_output=True).returncode == 0)
    if not sdl:
        out.append(('SDL2, the window the screen draws in', how['sdl2']))
    return out


def interpreter():
    """A Python for the bench's own: the newest of 3.13, 3.12 and 3.11 on this computer (ESPHome's own range), else
    the one running this."""
    for name in ('python3.13', 'python3.12', 'python3.11'):
        found = shutil.which(name)
        if found:
            return found
    return sys.executable


def setup(tree):
    """Everything the bench needs: the system's part checked, its own Python with ESPHome made or brought up to date."""
    lacking = missing()
    if lacking:
        say('The bench needs a few things this computer does not have yet:')
        for what, how in lacking:
            say(f'  - {what}:\n      {how}')
        stop('install them, then run python3 tools/preview.py --setup again')
    version = esphome_version(tree)
    python = python_of_venv()
    have = ''
    if python.exists():
        have = subprocess.run([str(python), '-c', 'import esphome.const as c; print(c.__version__)'],
                              capture_output=True, text=True).stdout.strip()
    if have != version:
        say(f'Making the bench\'s Python with ESPHome {version} in {VENV} (a few minutes, once) ...')
        wanted = [f'esphome=={version}', 'pillow', 'aiohttp>=3.12,<4', 'pyyaml']
        uv = shutil.which('uv')
        if uv:   # uv picks a Python ESPHome supports and installs in seconds
            if not python.exists():
                run([uv, 'venv', '--quiet', '--python', '3.13', str(VENV)])
            run([uv, 'pip', 'install', '--quiet', '--python', str(python), *wanted])
        else:
            if not python.exists():
                run([interpreter(), '-m', 'venv', str(VENV)])
            run([str(python), '-m', 'pip', 'install', '--quiet', '--upgrade', 'pip'])
            run([str(python), '-m', 'pip', 'install', '--quiet', *wanted])
    say(f'Ready: ESPHome {version}, Tessera {REF if not os.environ.get("TESSERA_TREE") else tree}.')
    say('The first build of each screen takes a few minutes (ESPHome fetches its parts once); after that only what '
        'changed is built again.')


def plugin_folder(args):
    """The plugin to bench: the first argument that is a folder with a manifest, else the folder you are in."""
    for i, arg in enumerate(args):
        if not arg.startswith('-') and (Path(arg) / 'tessera-plugin.yaml').is_file():
            return Path(arg).resolve(), args[:i] + args[i + 1:]
    here = Path.cwd()
    if (here / 'tessera-plugin.yaml').is_file():
        return here, args
    known = sorted(p.name for p in (ROOT / 'plugins').iterdir() if (p / 'tessera-plugin.yaml').is_file()) if (ROOT / 'plugins').is_dir() else []
    stop('name the plugin\'s folder (the one with tessera-plugin.yaml), or run it from inside that folder'
         + (f'; in this repository: {", ".join("plugins/" + k for k in known)}' if known else ''))


def main():
    args = sys.argv[1:]
    if args[:1] in (['-h'], ['--help']):
        say(__doc__)
        say('Everything after the folder goes to the bench; its own options:')
        tree = core()
        if python_of_venv().exists():
            subprocess.run([str(python_of_venv()), str(BENCH), '--help'], env={**os.environ, 'TESSERA_TREE': str(tree)})
        else:
            say('  (run python3 tools/preview.py --setup first)')
        return 0
    tree = core()
    if '--setup' in args:
        setup(tree)
        return 0
    if '--list' in args:
        if not python_of_venv().exists():
            setup(tree)
        return subprocess.run([str(python_of_venv()), str(BENCH), 'x', '--list'], env={**os.environ, 'TESSERA_TREE': str(tree)}).returncode
    if not python_of_venv().exists() or missing():
        setup(tree)
    folder, rest = plugin_folder(args)
    if not os.environ.get('TESSERA_TREE') and not os.environ.get('TESSERA_REF') and wanted(folder) > offered(tree):
        need = '.'.join(map(str, wanted(folder)))
        say(f'{folder.name} names plugin API {need}, newer than the released firmware ({".".join(map(str, offered(tree)))}): '
            'building on Tessera\'s dev, which comes with the next release')
        tree = core('dev')
        if wanted(folder) > offered(tree):
            stop(f'not even Tessera\'s dev offers plugin API {need}')
    open_page = '--open' in rest
    rest = [a for a in rest if a != '--open']
    env = {**os.environ, 'ESPHOME': str(esphome_of_venv()), 'TESSERA_TREE': str(tree)}
    code = subprocess.run([str(python_of_venv()), str(BENCH), str(folder), *rest], env=env).returncode
    page = folder / '.preview' / 'index.html'
    if '--out' in rest:
        page = Path(rest[rest.index('--out') + 1]).resolve() / 'index.html'
    if open_page and page.is_file():
        webbrowser.open(page.as_uri())
    return code


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        stop(f'{" ".join(map(str, error.cmd))} failed ({error.returncode})')
    except KeyboardInterrupt:
        raise SystemExit(130)
