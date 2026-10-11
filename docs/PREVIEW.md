# The plugin bench

A plugin goes onto many screens: a 2.8-inch CYD lying down, a 4-inch square, a 4.3-inch standing up, a 10-inch panel,
each with its own pixels, density, look and grid, in light and in dark. The bench shows your plugin on all of them in a
few minutes, without a screen, and checks what it draws.

It builds the real firmware of each screen with your plugin in it, for your own computer, gives the tiles the data
of your `preview.yaml` the way the Tessera app would, and photographs everything your plugin adds:

- every tile at every size it offers (`sizes` in the manifest), on every screen and grid that takes that size, light
  and dark;
- the card a tap on each tile opens, and every card of the manifest opened by its id, light and dark;
- its top bar items, with their words and as their icon alone;
- its pages on the screen's settings page (Settings, Plugins);
- the full pages, light and dark.

It reads what your plugin adds from its manifest and from its code (`add_tile`, `add_card`, `add_bar_item`,
`add_tap_action`, `settings()`, `tessera::action`), and renders only what is there. And it checks:

- a part of a tile or a card outside its area;
- a label cut with dots;
- a character the font does not have (it draws as nothing);
- a word too faint to read on its ground, in light and in dark (a colour `on_theme` forgot, most often);
- two parts over each other (a number under a bar), and a label lower than its own letters;
- a tile, card or top bar item the code registers and the manifest does not name, or the other way round;
- an action the code calls that `permissions.home_assistant_actions` does not name;
- `Font::DIGITS` in code whose manifest names an API before 0.9;
- a question to Home Assistant without an answer in `preview.yaml`, and a tile that waits for data it never gets.

Everything lands in your plugin's folder under `.preview/`: `index.html` to look at it all, `overview.png` with every
tile at every size on one picture, and `summary.json` with the same as data, for an assistant or a script.

## Set it up once

The bench needs macOS or Linux, Python 3.11 or newer, a C++ compiler, SDL2 and git. On Windows it runs in WSL 2, the
Linux that comes with Windows (below): ESPHome builds the firmware for a computer on Linux and macOS only.

| System | Install |
|---|---|
| macOS | `xcode-select --install`, then with [Homebrew](https://brew.sh): `brew install sdl2 uv` |
| Ubuntu, Debian, WSL 2 | `sudo apt install build-essential libsdl2-dev git python3 python3-venv` |
| Fedora | `sudo dnf install gcc-c++ make SDL2-devel git python3` |

**Windows**, once:

1. Open PowerShell as administrator and run `wsl --install`, then restart Windows.
2. Open **Ubuntu** from the Start menu, choose a user name and a password, and run
   `sudo apt update && sudo apt install -y build-essential libsdl2-dev git python3 python3-venv`.

Then run the bench from Windows as from anywhere else, `py tools\preview.py plugins\my_idea` in PowerShell or the
terminal of your editor: it runs itself in WSL, with the paths made WSL's. Or run it in Ubuntu directly. Its Python and
its builds live in Ubuntu's home (`~/.cache/tessera-plugins`), where a build is many times quicker than on the Windows
drive; the pictures still land in your plugin's `.preview\`, and `--open` shows them in Windows' browser. `--window`
needs Windows 11, whose WSL shows Linux windows on the desktop.

[uv](https://docs.astral.sh/uv/) is optional; with it the bench makes its Python in seconds and picks a version
ESPHome supports by itself.

Then, in this repository:

```sh
python3 tools/preview.py --setup
```

It says what is still missing, with the command to install it. When nothing is, it makes a Python of its own with
the ESPHome that Tessera builds screens with (in `tools/.cache/preview-venv`). Nothing is installed outside this
repository but what the table above names.

The bench is this repository's (`tools/bench.py`); the firmware it builds is Tessera's own. It fetches that from
Tessera's repository by itself, into `tools/.cache/tessera-main`, and again when its copy is an hour old: `main`, the
firmware every screen runs. A plugin whose manifest names a plugin API newer than `main` offers (0.9 for
`Font::DIGITS`) is built on Tessera's `dev` instead, which comes with the next release, and the bench says so.
`TESSERA_REF=dev` always takes `dev`; `TESSERA_TREE=../homeassistant_espscreen` takes a checkout of your own.

## Run it

```sh
python3 tools/preview.py plugins/my_idea
```

or from inside the plugin's folder:

```sh
cd plugins/my_idea
python3 ../../tools/preview.py --open
```

A plugin in a repository of your own works the same: `python3 tools/preview.py ../my-plugin`.

The first build of each screen takes a few minutes, as ESPHome fetches its parts once. After that a run builds only
what changed: about half a minute per screen.

| Option | What |
|---|---|
| (none) | Four screens that differ the most: the CYD (2.8 inches, the compact look), the Guition (4 inches, square), the Waveshare 4.3 inches standing up, and the Guition 10.1 inches. |
| `--board <key>` | A board of Tessera's catalog, `-portrait` for one standing up (`waveshare43-portrait`). More than once for several. `--list` lists them. |
| `--all` | Every board, lying down and standing up. Long the first time. |
| `--screen 1024x600@7` | A glass of your own: pixels and inches (`@7`) or pixels and dpi (`:170`), lying as given. The look and the grid are the ones Tessera would give a board of that glass; add `/compact` or `/standard` to choose the look. More than once for several. |
| `--grid 4x3`, `--grid max` | Another grid on every screen that takes it, besides its own: a person chooses columns and rows per screen in the editor. `max` is the finest grid each screen takes, where your tile is smallest. |
| `--open` | Open `index.html` in your browser when it is done. |
| `--window` | Keep one screen open in its window afterwards: tap and swipe it with the mouse. The data goes again every 15 seconds, as the app sends it. |
| `--watch` | Build and photograph again whenever a file of the plugin changes. With `--window`, the window comes back with the new build. |
| `--live` | Ask the web services of your fetches themselves instead of `preview.yaml`, through the app's own fetcher and its rules. A secret input comes from the environment: `TESSERA_SECRET_<INPUT ID>=...`. |
| `--out <folder>` | Somewhere else than `.preview/`. |

The page `index.html` has buttons for light, dark or both, and for the size of the pictures: **Real size** shows each
picture as large as it is on its glass (by the glass's density), **Pixels** one pixel of the glass as one pixel of
yours, **Fit** everything small enough to compare at a glance.

## For an assistant (Claude Code and others)

The bench is how an assistant sees what it draws. Run it after every change to the plugin's C++, its manifest or its
`preview.yaml`, before saying a plugin is done:

```sh
python3 tools/preview.py --setup                  # once; it says what to install when something lacks
python3 tools/preview.py plugins/<id> --strict    # or from the plugin's folder: python3 <plugins repo>/tools/preview.py . --strict
```

- **It takes a while.** The first build of each of the four default screens takes a few minutes, later runs about half
  a minute each. Give the command a timeout of 20 minutes, or run it in the background and wait for it. A single
  `--board cyd` is the quickest round while the C++ still changes; the four defaults (or `--all`) before you are done.
- **Never `--window` or `--watch`.** Both wait for a person and never end on their own.
- **The check comes first.** The bench runs `tools/check.py` on the plugin with its own Python (which has PyYAML) and
  stops when it fails, so a plugin the app would refuse is never benched.
- **The exit code says it.** 0: every screen built and nothing to fix. 1: the check or a build failed, or the plugin
  cannot be benched (its reason is printed). 2 (with `--strict`): it built, and a finding is a warning.
- **Read the findings first.** They are printed at the end, one line each (`warning: guition, Waste 2x1, page 1,
  dark: 1 too faint to read on its ground: faint[Tomorrow]`), and are in `.preview/summary.json`.
- **Then look.** `.preview/overview.png` has every tile at every size on every screen on one picture. Each picture is
  also its own file: `.preview/<screen>/tile-<example>-<size>-<light|dark>.png`, `card-<id>-<theme>.png`,
  `tap-<example>-<size>.png`, `bar-<theme>.png`, `bar-icon-<theme>.png`, `settings-<n>.png`, `page-<n>-<theme>.png`; a
  grid of `--grid` has a folder of its own under the screen (`.preview/guition/4x5/`). Look at the smallest screen
  (`cyd`) and the largest, light and dark: a finding only catches what can be measured, a picture shows what looks wrong.
- **Give it real data.** Without a `preview.yaml` the tiles wait for data and the pictures show nothing of what the
  plugin does. Copy a real answer of the web service into `answers`, real attributes into `states`.
- **Say what was not benched.** A plugin with audio or a camera does not build there (exit 1 with a sentence); say so,
  and that it needs a test on a screen.

`summary.json`:

| Field | What |
|---|---|
| `plugin`, `version`, `rendered` | The plugin and when the bench ran. |
| `adds` | What the plugin adds: `tiles` (id, name, sizes, data, memory), `cards`, `bar_items`, `tap_actions`, `settings_entities`, `settings_rows`, `questions`, `actions`, `large_digits`, and `mismatches` between manifest and code. |
| `screens[]` | Each screen: `key`, `title`, `width`, `height`, `dpi`, `look`, `error` when it failed, and its `views`. |
| `screens[].views[]` | Each grid of it: `grid`, `folder` (empty for its own grid), `tiles[]` (`name`, `span` as `2x1`, `size`, `px`, the `light` and `dark` file), `cards[]`, `taps[]` (with the `actions` a tap asked Home Assistant for), `bar`, `bar_icon`, `settings[]`, `pages[]`. |
| `findings[]` | `level` (`error`, `warning` or `info`), `screen`, `where` and `text`. Fix every `error` and `warning`; an `info` says what was not shown and why. |

## preview.yaml: the data your plugin is shown with

Without one, every tile type is shown once, with its options' defaults and no data: the waiting state. Put a
`preview.yaml` beside the manifest to show it with data. Every part is optional.

```yaml
tiles:                         # the tiles to show; each at every size it offers, unless `sizes` says which
  - tile: next                 # a tile id of the manifest
    name: Centraal Station     # the name a person gives it (default: the tile's name)
    options: { stop: "30005002", walk: 3 }   # its options, as the inspector sets them
    sizes: [1x1, 3x2]          # optional
  - tile: next
    name: No departures
    options: { stop: "30005002" }
    sizes: [2x1]
    answers: { departures: { "30005002": { Passes: {} } } }   # this one's own answer: an empty stop
  - tile: chart
    entity: sensor.energy_price   # a tile of an entity: the entity it is given

answers:                       # the answer of each fetch, by its id, as the web service gives it (its JSON)
  departures:
    "30005002":
      Passes:
        a: { LinePublicNumber: "2", DestinationName50: "Nieuwegein-Zuid", ExpectedDepartureTime: "{now+4m}" }

states:                        # entities, as Home Assistant has them
  sensor.energy_price:
    state: "0.24"
    attributes: { unit_of_measurement: EUR/kWh, today: [0.21, 0.24, 0.31] }

commands:                      # answers to the questions of permissions.ha_commands (tessera::send)
  "call_service:calendar.get_events":
    calendar.waste: { events: [{ start: "{now+1d}", summary: Paper }] }

cards:                         # the entity and title a card opens with, when the manifest's card needs one
  - { card: upcoming, entity: calendar.waste }

time_zone: Europe/Amsterdam    # the zone of the moments below (default Europe/Amsterdam)
```

- An **answer** goes through your fetch's `map` exactly as in the app, so it is the web service's own JSON, not what
  the screen gets. Copy one from the service once and keep it here.
- **States** reach the tiles of an entity as the app sends them (the attributes the manifest names, bounded), and
  every entity your `plugin.yaml` reads itself (a `homeassistant` sensor) as Home Assistant would send it.
- **Moments** are written from the time of the run, so a countdown never runs out: `"{now+5m}"` is the local time in
  five minutes as text (`2026-10-11T15:20:00`), `"{now-1d}"` a day ago, `"{epoch+2h}"` in two hours as seconds since
  1970 (a number when it is the whole value). Units: `s`, `m`, `h`, `d`.
- A tile's `data:` gives what the screen gets as it is, past the map: `data: { wait: failed }` shows its failed state.
- Never put a secret here: the file is shared with your plugin.

[`plugins/ov_departures/preview.yaml`](../plugins/ov_departures/preview.yaml) (a fetch) and
[`plugins/waste_collection/preview.yaml`](../plugins/waste_collection/preview.yaml) (an entity, a card that asks Home
Assistant, a top bar item) are complete examples. The template has one to start from.

## What the bench cannot show

- **Audio and cameras.** The firmware is built for your computer, which has no speaker, microphone or camera of a
  screen: a plugin that needs or brings one of those features (`requires.features`, `provides`) is not built, and the
  bench says so. Test it on a screen (TESTING.md). A plugin with switches or sensors on a board's pins builds, and its
  settings rows show; a plugin for some boards only (`boards`) is shown on those.
- **The real Home Assistant and the real services**, unless `--live`: it shows what `preview.yaml` gives.
- **Speed and memory on the chip.** The pictures are the firmware's own, the timing and the memory are your
  computer's: a tile's `memory` in the manifest, and the flash a plugin costs on a 4 MB board, show on a screen only.
- **A finger on the glass.** Tap and swipe in `--window`, then try it on a real screen before you publish.

A top bar item stands beside the page's name. On a page with a long name a screen leaves an item out that does not fit;
the bench names its page "Home", so the item shows.

## Common findings

| The bench says | Usually |
|---|---|
| too faint to read on its ground, dark | `on_theme` does not set the colour of that label again. A screen with memory to spare keeps its pages and only calls `on_theme`; a small one builds the tile anew, which hides the mistake there. |
| cut with dots | The text is longer than the room on the smallest screen or the finest grid. Take a smaller font there (`ui::text_width`), or a shorter text. |
| with a character its font lacks | `Font::DIGITS` with a letter, or a sign the screen's fonts do not carry. Test with `ui::covers(text, Font::DIGITS)` and step down to `VALUE`. |
| outside its area | A position or size worked out from a fixed number instead of `TileContext`'s `width` and `height`. |
| over another part | Two parts on one place: a number under a bar, two lines on top of each other. On a short tile (the finest grid, `--grid max`) something has to give way: a line, then the name. |
| lower than its letters | A label given less height than its font's line: its letters are cut off. Take its height from `ui::line_height`, or a smaller font. |
| not on a 1 x 4 grid | The grid has no room for that size (a 2x1 tile on one column). Nothing to fix: the editor never offers it there. |
| the tile waits (asking) | `preview.yaml` has no answer for the tile's fetch. |
