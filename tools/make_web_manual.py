#!/usr/bin/env python3
"""Writes docs/manual/index.html, the browsable web version of the manual, from docs/manual/manual.html (the source of
the PDF): same text, tables and pictures; the print cover is replaced by a site header, the contents become a side menu.

    python3 tools/make_web_manual.py            # write
    python3 tools/make_web_manual.py --check    # fail if the committed file is out of date
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "manual" / "manual.html"
OUT = ROOT / "docs" / "manual" / "index.html"

LINKS = [("Firmware builder", "../"), ("PDF manual", "../Modded-Cycles-Techno-Edition-Manual.pdf"),
         ("GitHub", "https://github.com/mbreilly/Modded_cycles_techno_edition"),
         ("SoundCloud: m_reilly", "https://soundcloud.com/m_reilly")]

SCREEN_CSS = """
@media screen {
  html { font-size: 9pt; background: #f4f3f0; scroll-padding-top: 72px; }
  body { margin: 0; }
  .site-top { position: sticky; top: 0; z-index: 5; background: #1f252c; color: #eef0f2; }
  .site-top .in { max-width: 1280px; margin: 0 auto; padding: 12px 16px; display: flex; flex-wrap: wrap;
                  align-items: center; gap: 8px 20px; font: 600 14px/1.3 Inter, system-ui, sans-serif; }
  .site-top .brand { display: flex; align-items: center; gap: 10px; color: #eef0f2; text-decoration: none; margin-right: auto; }
  .site-top .brand i { display: inline-grid; grid-template-columns: 8px 8px; gap: 2px; }
  .site-top .brand i b { width: 8px; height: 8px; border-radius: 2px; background: #3a434e; }
  .site-top .brand i b.a { background: var(--amber); }
  .site-top a.l { color: #c9ced4; text-decoration: none; font-weight: 500; }
  .site-top a.l:hover { color: var(--amber); }
  .site-top a.sc { color: var(--amber); }
  .layout { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 0 32px;
            padding: 0 16px; }
  nav.toc { position: sticky; top: 52px; align-self: start; max-height: calc(100vh - 52px); overflow: auto;
            padding: 20px 4px 40px 0; page-break-before: auto; zoom: 1.25; }
  nav.toc h1 { font-size: 12pt; margin: 0 0 4mm; }
  main.manual { background: #fff; padding: 28px 40px 60px; margin: 20px 0 40px; border-radius: 10px;
                box-shadow: 0 1px 3px rgba(0,0,0,.08); min-width: 0; zoom: 1.4; }
  main.manual h1.ch { margin-top: 12mm; padding-top: 6mm; border-top: 1px solid #e3e1dc; }
  main.manual h1.ch:first-of-type { margin-top: 0; padding-top: 0; border-top: 0; }
  main.manual table { display: block; overflow-x: auto; max-width: 100%; }
  main.manual img { max-width: 100%; height: auto; }
  main.manual a { overflow-wrap: anywhere; }
  .web-intro { margin: 0 0 6mm; color: #5d656e; }
  @media (max-width: 900px) {
    .site-top { position: static; }
    html { scroll-padding-top: 8px; }
    .layout { display: block; padding: 0 8px; }
    nav.toc { position: static; max-height: none; zoom: 1.15; padding: 16px 8px; }
    main.manual { padding: 18px 14px 40px; zoom: 1.2; margin: 8px 0 24px; }
    .site-top .brand { margin-right: 0; width: 100%; }
  }
}
@media print { .site-top { display: none; } }
"""


def render():
    src = SRC.read_text(encoding="utf-8")
    head, body = src.split("</head>", 1)
    head = head.replace("<title>Modded Cycles Techno Edition Manual</title>",
                        "<title>Modded Cycles Techno Edition · Manual</title>"
                        '<meta name="viewport" content="width=device-width, initial-scale=1">'
                        '<link rel="preconnect" href="https://fonts.googleapis.com">'
                        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" '
                        'rel="stylesheet">')
    head = head.replace("</style>", SCREEN_CSS + "</style>", 1)
    body = re.sub(r'<div class="cover">.*?\n</div>\n', "", body, count=1, flags=re.S)
    m = re.search(r'<nav class="toc">.*?</nav>\n', body, re.S)
    if not m:
        sys.exit("!! contents (nav.toc) not found in manual.html")
    toc = m.group(0)
    rest = body[m.end():].replace("</body>", "").replace("</html>", "")
    pre = body[:m.start()].replace("<body>", "")
    links = "".join(f'<a class="l{" sc" if "soundcloud" in u else ""}" href="{u}">{t}</a>' for t, u in LINKS)
    top = ('<header class="site-top"><div class="in"><a class="brand" href="../"><i><b></b><b class="a"></b><b></b><b></b></i>'
           'Modded Cycles Techno Edition · Owner\'s manual</a>' + links + '</div></header>')
    intro = ('<p class="web-intro">The owner\'s manual for Modded Cycles Techno Edition 1.0 (first edition, November 2026), '
             'by <a href="https://soundcloud.com/m_reilly">m_reilly</a>. Also as a '
             '<a href="../Modded-Cycles-Techno-Edition-Manual.pdf">PDF</a>.</p>')
    return (head + "</head><body>" + pre + top + '<div class="layout">' + toc + '<main class="manual">' + intro
            + rest + "</main></div>\n<!-- Generated by tools/make_web_manual.py from manual.html. Do not edit by hand. -->\n"
            "</body></html>\n")


def main():
    text = render()
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            sys.exit(f"!! {OUT.relative_to(ROOT)} is out of date: run python3 tools/make_web_manual.py")
        print(f"{OUT.relative_to(ROOT)} is up to date")
        return
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
