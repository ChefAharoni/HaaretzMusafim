#!/usr/bin/env python3
"""Render the whole site to static files in dist/.

Usage: python build_static.py [--prefix /HaaretzMusafim]

Reads ALGOLIA_APP_ID and ALGOLIA_SEARCH_API_KEY (search-only key) from the
environment. Never uses the admin key and never copies data/ or *.json.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)  # the app reads data/ with relative paths

SITE = "https://haaretzarchive.com"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="", help="path prefix, e.g. /HaaretzMusafim")
    ap.add_argument("--out", default="dist")
    args = ap.parse_args()
    prefix = args.prefix.strip().rstrip("/")
    if prefix and not prefix.startswith("/"):
        prefix = "/" + prefix

    # Import here so cwd is already the repo root.
    from flask import render_template
    import app as appmod
    from modules.date_links import load_date_links

    app = appmod.app
    date_links = load_date_links()

    def static_show_links(date):
        titled, bare = date_links[date]
        return render_template(
            "links.html", date=date, weekend_urls=titled, only_urls=bare
        )

    app.view_functions["show_links"] = static_show_links

    out = ROOT / args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    client = app.test_client()
    # base_url path becomes SCRIPT_NAME, so url_for() emits prefixed links
    # (environ_base={"SCRIPT_NAME": ...} is overridden by the request builder).
    base_url = "http://localhost" + prefix
    written = []

    def render(route, rel, expect=200):
        resp = client.get(route, base_url=base_url)
        if resp.status_code != expect:
            sys.exit(f"{route}: status {resp.status_code}, expected {expect}")
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(resp.data)
        written.append(rel)

    render("/", "index.html")
    render("/ads", "ads.html")
    render("/privacy_policy", "privacy_policy.html")
    render("/__not_found__", "404.html", expect=404)

    n_segments = n_years = 0
    for segment, dates in appmod.grouped_dates.items():
        render(f"/segment/{segment}", f"segment/{segment}.html")
        n_segments += 1
        for year in sorted({int(d.split("-")[0]) for d in dates}):
            render(f"/segment/{segment}/{year}", f"segment/{segment}/{year}.html")
            n_years += 1

    all_dates = sorted(date_links)
    for date in all_dates:
        render(f"/date/{date}", f"date/{date}.html")

    shutil.copytree(
        ROOT / "static", out / "static",
        ignore=shutil.ignore_patterns(
            ".DS_Store", "*.json", ".env*",
            # dead, unreferenced scripts that still call /env-config
            "autocomplete.js", "getAlgoliaResults.js",
        ),
    )

    (out / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8"
    )
    urls = ["/", "/ads", "/privacy_policy"]
    for segment, dates in appmod.grouped_dates.items():
        urls.append(f"/segment/{segment}")
        urls += [f"/segment/{segment}/{y}"
                 for y in sorted({int(d.split('-')[0]) for d in dates})]
    urls += [f"/date/{d}" for d in all_dates]
    body = "\n".join(f"  <url><loc>{SITE}{u}</loc></url>" for u in urls)
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n",
        encoding="utf-8",
    )

    print(
        f"Built {len(written)} pages into {out} "
        f"(segments={n_segments}, segment-years={n_years}, dates={len(all_dates)}, "
        f"prefix={prefix!r})"
    )


if __name__ == "__main__":
    main()
