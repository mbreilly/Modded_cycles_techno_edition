# Manual source

`manual.html` is the source of [`../Modded-Cycles-Techno-Edition-Manual.pdf`](../Modded-Cycles-Techno-Edition-Manual.pdf)
(A4, styles inline, images in `img/`). To rebuild the PDF after an edit:

```sh
pip install weasyprint
python3 -c "from weasyprint import HTML; HTML('docs/manual/manual.html').write_pdf('docs/Modded-Cycles-Techno-Edition-Manual.pdf')"
```

It uses the Inter font when it is installed and falls back to a sans-serif font otherwise.
The plug-in screenshots in `img/` show the Modded Cycles Techno Edition plug-in window.

After an edit, also run `python3 tools/make_web_manual.py`: it writes `index.html`, the browsable manual of the
website (CI checks it is up to date).
