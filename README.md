# Musafei Haaretz

<div align="center">
<img src="https://raw.githubusercontent.com/ChefAharoni/HaaretzMusafim/main/assets/ArchiveLogo.svg" alt="Archive Logo" width="200" height="100" >
</div> <br />

[![Monthly Data Update](https://github.com/ChefAharoni/HaaretzMusafim/actions/workflows/deploy.yml/badge.svg)](https://github.com/ChefAharoni/HaaretzMusafim/actions/workflows/deploy.yml)

Since Haaretz doesn't provide a an organized archive for their Musafim (weekend magazines), this repo takes each week's url of the magazine, and displays it as a list.

Search is client-side [Algolia](https://www.algolia.com/).

Hosted at: https://haaretzarchive.com (static site on GitHub Pages behind Cloudflare).

Built with [Flask](https://flask.palletsprojects.com/en/3.0.x/) templates rendered to static HTML by `build_static.py`. A GitHub Actions workflow (`.github/workflows/deploy.yml`) scrapes new Haaretz sitemaps monthly, updates the Algolia index, builds and deploys.

Local build: `pip install -r requirements.txt`, set `ALGOLIA_APP_ID` and `ALGOLIA_SEARCH_API_KEY`, run `python build_static.py` (output in `dist/`).

Disclaimer:
This repo is not associated in any way with Haaretz, and does not illegaly distirbute its content. Its sole purpose is to organize the web pages in an archive, in a way it'll be easier to access them. 
A paid membership to Haaretz is still needed to view these magazines.

