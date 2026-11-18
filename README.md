# Nathan’s personal archive

Static HTML and CSS; no package installation or build step is required.

## Preview and verify

From the repository root:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
python3 scripts/check_archive.py
```

Open http://127.0.0.1:8765 in a browser. The check validates entry-page links,
anchors, writing coverage, and preservation of the original essays and assets.

## Editing the archive

- `index.html`: introduction, Delphic maxim, selected essays, and a credited
  image from the existing Simon Li interview.
- `archive.css`: shared responsive styling for the six archive entry pages.
- `Writings/Writing.html`: complete index of the 20 existing essays.
- `Projects/Projects Page.html`: original project names; unpublished items
  are text rather than empty links. The original music-section writing links
  now reach their actual essays.
- `Life.html`: seven planned photographic chapters. The repository does not
  yet contain these collections. Add real photographs, alt text, captions,
  dates when known, and credits before marking a chapter available. Keep
  the two Geronimo voyages separate.
- About and Contact retain the original introduction and contact details.
  The introduction is identified as historical rather than a current bio.

The original essay pages, image files, fonts, and `styles.css` are unchanged.
Their older reading layouts are outside this homepage/navigation redesign.
Professional case studies and the life-history photography require source
material before they can be published; none has been invented here.

Navigation works without JavaScript. The layout stacks at 800px, retains visible
navigation, includes a skip link and keyboard focus styles, and uses local fonts.
