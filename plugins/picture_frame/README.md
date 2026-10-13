# Picture frame

A tile that shows one picture: a person's photo from Home Assistant, an image entity, the cover of what a player
plays, or any picture at an address you give it (a film poster from The Movie Database, a photo from Unsplash). The
picture fills the tile, or shows whole, with the tile's name in its corner.

It is the smallest plugin with pictures on a tile, there to show how pictures reach a plugin's tile
([docs/FIRMWARE_API.md](../../docs/FIRMWARE_API.md), "Pictures on a tile"): the plugin lays out a place and names an
address; Tessera's app fetches the picture and the screen shows it. A plugin never fetches anything itself.

## Set up

1. Add the plugin to a screen in Tessera. The screen builds once.
2. In Layout, place the **Picture** tile from the library's Plugins group, at any size.
3. In the inspector, choose an entity whose picture it shows (a person, an image entity, a media player), or fill in
   the **Address** of a picture on `image.tmdb.org` or `images.unsplash.com`, such as
   `https://image.tmdb.org/t/p/w342/<poster>.jpg`. An address wins over the entity's picture.
4. **Fit**: cover fills the tile; contain shows the whole picture on the tile's own colour.

## Good to know

- A board without the memory for pictures (the CYD, the Waveshare 3.5-inch, the Hosyond 4-inch) shows "No picture"
  instead; the other boards show it.
- The picture comes once and stays while the tile is there; a new address, or a new picture of the entity, replaces it.
- A picture that does not come (a wrong address, a host that is down) leaves a soft block; the screen asks again
  later.

## Privacy

For an address you fill in, Tessera (the app in Home Assistant, not the screen) fetches that picture from
`image.tmdb.org` or `images.unsplash.com`, which see the address of your Home Assistant and the picture's address,
nothing else. An entity's own picture stays within Home Assistant. The screen never reaches the internet.
