"""Scrape NBA box scores from Basketball-Reference and build data/nba_games.csv.

Usage (run from backend/):
    python scripts/scrape_games.py fetch 2019 2025   # download schedule + box score pages
    python scripts/scrape_games.py parse             # build the games CSV from saved pages
"""
import os
import sys
import time
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = "https://www.basketball-reference.com"
DATA_DIR = os.environ.get("NBA_DATA_DIR", "data")
STANDINGS_DIR = os.path.join(DATA_DIR, "standings")
SCORES_DIR = os.path.join(DATA_DIR, "scores")
DELAY = 3.5  # Basketball-Reference allows about 20 requests a minute


def get_html(url, selector):
    """Return the inner HTML of `selector` on `url`, or None if the page can't be fetched."""
    for attempt in range(3):
        time.sleep(DELAY)
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        if r.status_code == 429:
            # rate limited: wait as long as the site asks (blocks can last an hour), then retry
            wait = int(r.headers.get("Retry-After", 3600))
            print(f"Rate limited, waiting {wait}s")
            time.sleep(wait)
            continue
        if r.ok:
            node = BeautifulSoup(r.text, "html.parser").select_one(selector)
            return str(node) if node else None
    return None


def save(url, path, selector):
    if os.path.exists(path):  # skip pages we already have
        return
    html = get_html(url, selector)
    if html:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)


def fetch(first_season, last_season):
    os.makedirs(STANDINGS_DIR, exist_ok=True)
    os.makedirs(SCORES_DIR, exist_ok=True)
    for season in range(first_season, last_season + 1):
        html = get_html(f"{BASE}/leagues/NBA_{season}_games.html", "#content .filter")
        months = [a["href"] for a in BeautifulSoup(html or "", "html.parser").find_all("a")]
        for href in months:
            save(BASE + href, os.path.join(STANDINGS_DIR, os.path.basename(href)), "#all_schedule")
    for month_file in sorted(os.listdir(STANDINGS_DIR)):
        with open(os.path.join(STANDINGS_DIR, month_file), encoding="utf-8") as f:
            links = BeautifulSoup(f.read(), "html.parser").find_all("a")
        for href in {a.get("href", "") for a in links if "boxscore" in a.get("href", "") and a["href"].endswith(".html")}:
            save(BASE + href, os.path.join(SCORES_DIR, os.path.basename(href)), "#content")


def parse_box_score(path):
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for row in soup.select("tr.over_header, tr.thead"):
        row.decompose()
    html = StringIO(str(soup))

    line_score = pd.read_html(html, attrs={"id": "line_score"})[0]
    cols = list(line_score.columns)
    cols[0], cols[-1] = "team", "total"
    line_score.columns = cols
    line_score = line_score[["team", "total"]]

    summaries = []
    for team in line_score["team"]:
        stats = [pd.read_html(StringIO(str(soup)), attrs={"id": f"box-{team}-game-{kind}"}, index_col=0)[0]
                 .apply(pd.to_numeric, errors="coerce") for kind in ("basic", "advanced")]
        totals = pd.concat([s.iloc[-1, :] for s in stats])  # last row is the team total
        maxes = pd.concat([s.iloc[:-1, :].max() for s in stats])  # best single player per stat
        totals.index = totals.index.str.lower()
        maxes.index = maxes.index.str.lower() + "_max"
        summary = pd.concat([totals, maxes])
        keep = [c for c in summary.index.drop_duplicates() if "bpm" not in c]
        summaries.append(summary[keep])

    game = pd.concat([pd.concat(summaries, axis=1).T.reset_index(drop=True), line_score], axis=1)
    game["home"] = [0, 1]  # line score lists the away team first
    opp = game.iloc[::-1].reset_index(drop=True)
    opp.columns = [c + "_opp" for c in opp.columns]
    full = pd.concat([game, opp], axis=1)

    nav = soup.select_one("#bottom_nav_container")
    full["season"] = int(os.path.basename(nav.find_all("a")[1]["href"]).split("_")[0][-4:]) if nav else None
    full["date"] = pd.to_datetime(os.path.basename(path)[:8], format="%Y%m%d")
    full["won"] = full["total"] > full["total_opp"]
    return full


def parse():
    files = sorted(f for f in os.listdir(SCORES_DIR) if f.endswith(".html"))
    games, failed = [], []
    for i, name in enumerate(files):
        try:
            games.append(parse_box_score(os.path.join(SCORES_DIR, name)))
        except Exception as e:
            failed.append((name, e))
        if i % 500 == 0:
            print(f"{i}/{len(files)}")
    df = pd.concat(games, ignore_index=True)
    out = os.path.join(DATA_DIR, "nba_games.csv")
    df.to_csv(out)
    print(f"Parsed {len(games)} of {len(files)} box scores ({len(df)} team-game rows) -> {out}")
    for name, e in failed:
        print("FAILED", name, e)


if __name__ == "__main__":
    if sys.argv[1:2] == ["fetch"]:
        fetch(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1:2] == ["parse"]:
        parse()
    else:
        print(__doc__)
