#!/usr/bin/env python3
"""Site-level SEO check: robots.txt, sitemaps, and HTTPS/www redirect behavior (stdlib only).

Usage:
  python site_check.py https://example.com
  python site_check.py https://example.com --json

Limitations: fetches robots.txt and up to --max-urls sitemap URLs (default 25) and reports
status codes. It does not render pages, check indexation, or replace a full crawler.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; SEO-Skill-Scanner/1.0; +https://agentskills.io)"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def fetch(url, follow=True, method="GET", limit=2_000_000):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    opener = urllib.request.build_opener() if follow else urllib.request.build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=15) as r:
            body = r.read(limit) if method == "GET" else b""
            if body[:2] == b"\x1f\x8b":
                body = gzip.decompress(body)
            return r.status, dict(r.headers), body.decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), "", url
    except Exception as e:  # network/DNS/TLS
        return 0, {}, str(e), url


def parse_robots(text):
    """Return (sitemap_urls, disallow_all) from robots.txt text."""
    sitemaps = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", text)
    disallow_all = bool(re.search(r"(?im)^\s*disallow:\s*/\s*$", text))
    return sitemaps, disallow_all


def parse_sitemap(body):
    """Return (is_index, locs) for sitemap XML text."""
    return "<sitemapindex" in body, re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)


def check(origin, max_urls=25):
    p = urllib.parse.urlparse(origin)
    out = {"origin": origin, "issues": [], "notes": []}

    st, _, robots, _ = fetch(origin + "/robots.txt")
    out["robots_status"] = st
    sitemaps, disallow_all = parse_robots(robots) if st == 200 else ([], False)
    if st != 200:
        out["issues"].append(f"robots.txt returned {st}")
    elif disallow_all:
        out["issues"].append("robots.txt contains 'Disallow: /' - verify it is not applied to all crawlers in production")
    if st == 200 and not sitemaps:
        out["notes"].append("No Sitemap: directive in robots.txt")
    if not sitemaps:
        sitemaps = [origin + "/sitemap.xml"]

    urls, seen = [], set()
    queue = list(sitemaps)
    while queue and len(seen) < 10:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        s, _, body, _ = fetch(sm)
        if s != 200:
            out["issues"].append(f"Sitemap {sm} returned {s}")
            continue
        is_index, locs = parse_sitemap(body)
        if is_index:
            queue += locs
        else:
            urls += locs
    out["sitemaps_checked"] = sorted(seen)
    out["sitemap_url_count"] = len(urls)

    bad = []
    for u in urls[:max_urls]:
        s, h, _, _ = fetch(u, follow=False, method="HEAD")
        if s != 200:
            bad.append({"url": u, "status": s, "location": h.get("Location")})
    if bad:
        out["issues"].append(f"{len(bad)} of first {min(len(urls), max_urls)} sitemap URLs are not 200")
    out["sitemap_non_200"] = bad

    if p.scheme == "https":
        s, h, _, _ = fetch("http://" + p.netloc, follow=False, method="HEAD")
        out["http_to_https"] = {"status": s, "location": h.get("Location")}
        if not (300 <= s < 400 and (h.get("Location") or "").startswith("https://")):
            out["issues"].append("http:// does not redirect to https://")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-urls", type=int, default=25)
    a = ap.parse_args()

    p = urllib.parse.urlparse(a.url if "//" in a.url else "https://" + a.url)
    out = check(f"{p.scheme}://{p.netloc}", a.max_urls)

    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"Origin: {out['origin']}\nrobots.txt: {out['robots_status']}\nSitemap URLs found: {out['sitemap_url_count']}")
        for i in out["issues"]:
            print("ISSUE:", i)
        for n in out["notes"]:
            print("NOTE:", n)
        if not out["issues"]:
            print("No issues detected by this lightweight check.")


if __name__ == "__main__":
    main()
