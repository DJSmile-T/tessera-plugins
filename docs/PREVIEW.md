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
- a tile, card or top bar item the code registers and the manifest does not name, or the other way round;
- an action the code calls that `permissions.home_assistant_actions` does not name;
- `Font::DIGITS` in code whose manifest names an API before 0.9;
- a question to Home Assistant without an answer in `preview.yaml`, and a tile that waits for data it never gets.

Everything lands in your plugin's folder under `.preview/`: `index.html` to look at it all, `overview.png` with every
tile at every size on one picture, and `summary.json` with the same as data, for an assistant or a script.

## Set it up once

The bench needs a Mac or Linux (on Windows: WSL 2 with Ubuntu), Python 3.11 or newer, a C++ compiler, SDL2 and git.

| System | Install |
|---|---|
| macOS | `xcode-select --install`, then with [Homebrew](https://brew.sh): `brew install sdl2 uv` |
| Ubuntu, Debian, WSL 2 | `sudo apt install build-essential libsdl2-dev git python3 python3-venv` |
| Fedora | `sudo dnf install gcc-c++ make SDL2-devel git python3` |

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
- **Speed and memory on the chip.** The pictures are the firmware's own, the timing is your computer's. The screens
  table says how much of the screen's layout memory the bench's layout takes, as the screen counts it.
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
| not on a 1 x 4 grid | The grid has no room for that size (a 2x1 tile on one column). Nothing to fix: the editor never offers it there. |
| the tile waits (asking) | `preview.yaml` has no answer for the tile's fetch. |
