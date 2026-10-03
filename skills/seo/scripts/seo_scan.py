#!/usr/bin/env python3
"""Lightweight deterministic SEO scanner using Python stdlib only.

Usage:
  python seo_scan.py https://example.com
  python seo_scan.py https://example.com --json

This is intentionally small. It does not replace browser rendering, Search Console,
field Core Web Vitals, a full crawler, or search-engine index inspection.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; SEO-Skill-Scanner/1.0; +https://agentskills.io)"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta = []
        self.links = []
        self.images = []
        self.headings = []
        self.canonicals = []
        self.alternates = []
        self.jsonld = []
        self._script_type = None
        self._script_buf = []

    def handle_starttag(self, tag, attrs):
        d = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.meta.append(d)
        elif tag == "a":
            self.links.append(d)
        elif tag == "img":
            self.images.append(d)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.append((tag, []))
        elif tag == "link":
            rel = {x.strip().lower() for x in d.get("rel", "").split()}
            if "canonical" in rel and d.get("href"):
                self.canonicals.append(d["href"])
            if "alternate" in rel and d.get("href"):
                self.alternates.append(d)
        elif tag == "script":
            self._script_type = d.get("type", "").lower()
            if self._script_type == "application/ld+json":
                self._script_buf = []

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._script_type == "application/ld+json":
            raw = "".join(self._script_buf).strip()
            if raw:
                self.jsonld.append(raw)
            self._script_type = None
            self._script_buf = []

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self.headings and self.lasttag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings[-1][1].append(data)
        if self._script_type == "application/ld+json":
            self._script_buf.append(data)


def fetch(url: str, timeout: int = 15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*;q=0.8"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        body = r.read(3_000_000)
        return {
            "final_url": r.geturl(),
            "status": getattr(r, "status", None),
            "headers": dict(r.headers.items()),
            "body": body,
        }


def meta_value(meta, *, name=None, prop=None):
    for m in meta:
        if name and m.get("name", "").lower() == name.lower():
            return m.get("content", "").strip()
        if prop and m.get("property", "").lower() == prop.lower():
            return m.get("content", "").strip()
    return ""


def scan(url: str):
    out = {"input_url": url, "errors": [], "warnings": [], "info": {}}
    try:
        r = fetch(url)
    except urllib.error.HTTPError as e:
        out["errors"].append(f"HTTP error: {e.code} {e.reason}")
        out["info"]["status"] = e.code
        return out
    except Exception as e:
        out["errors"].append(f"Fetch failed: {e}")
        return out

    final_url = r["final_url"]
    status = r["status"]
    ctype = r["headers"].get("Content-Type", "")
    out["info"].update({"status": status, "final_url": final_url, "content_type": ctype})
    if final_url != url:
        out["info"]["redirected"] = True
    if status != 200:
        out["warnings"].append(f"Final response status is {status}, not 200")
    if "text/html" not in ctype.lower():
        out["warnings"].append("Response does not advertise text/html; HTML checks may be unreliable")

    enc = "utf-8"
    m = re.search(r"charset=([\w-]+)", ctype, re.I)
    if m:
        enc = m.group(1)
    html = r["body"].decode(enc, errors="replace")

    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:
        out["warnings"].append(f"HTML parser warning: {e}")

    title = re.sub(r"\s+", " ", p.title).strip()
    desc = meta_value(p.meta, name="description")
    robots = meta_value(p.meta, name="robots")
    googlebot = meta_value(p.meta, name="googlebot")
    h1s = [re.sub(r"\s+", " ", "".join(parts)).strip() for tag, parts in p.headings if tag == "h1"]

    out["info"].update({
        "title": title,
        "title_length": len(title),
        "meta_description": desc,
        "meta_description_length": len(desc),
        "meta_robots": robots,
        "meta_googlebot": googlebot,
        "x_robots_tag": r["headers"].get("X-Robots-Tag", ""),
        "canonicals": p.canonicals,
        "h1": h1s,
        "links": len(p.links),
        "images": len(p.images),
        "jsonld_blocks": len(p.jsonld),
    })

    if not title:
        out["errors"].append("Missing <title>")
    if len(p.canonicals) > 1:
        out["warnings"].append("Multiple canonical link tags found")
    if not p.canonicals:
        out["warnings"].append("No canonical link tag found (not always an error, but verify intent)")
    if len(h1s) == 0:
        out["warnings"].append("No H1 found in fetched HTML")
    if len(h1s) > 1:
        out["info"]["multiple_h1_note"] = "Multiple H1s are not inherently an SEO error; verify document clarity."
    if not desc:
        out["warnings"].append("No meta description found")

    directives = " ".join([robots, googlebot, r["headers"].get("X-Robots-Tag", "")]).lower()
    if "noindex" in directives:
        out["warnings"].append("A noindex directive is present")

    missing_alt = sum(1 for img in p.images if "alt" not in img)
    empty_alt = sum(1 for img in p.images if img.get("alt", None) == "")
    out["info"]["images_missing_alt_attribute"] = missing_alt
    out["info"]["images_empty_alt"] = empty_alt

    parsed = urllib.parse.urlparse(final_url)
    internal = external = non_http = 0
    targets = Counter()
    for a in p.links:
        href = a.get("href", "").strip()
        if not href:
            continue
        absu = urllib.parse.urljoin(final_url, href)
        pu = urllib.parse.urlparse(absu)
        if pu.scheme not in {"http", "https"}:
            non_http += 1
            continue
        if pu.netloc == parsed.netloc:
            internal += 1
            targets[urllib.parse.urlunparse((pu.scheme, pu.netloc, pu.path, "", pu.query, ""))] += 1
        else:
            external += 1
    out["info"].update({"internal_links": internal, "external_links": external, "non_http_links": non_http})

    bad_jsonld = 0
    jsonld_types = []
    for raw in p.jsonld:
        try:
            data = json.loads(raw)
            nodes = data if isinstance(data, list) else [data]
            for node in nodes:
                if isinstance(node, dict):
                    t = node.get("@type")
                    if t:
                        jsonld_types.extend(t if isinstance(t, list) else [t])
        except Exception:
            bad_jsonld += 1
    out["info"]["jsonld_types"] = jsonld_types
    if bad_jsonld:
        out["warnings"].append(f"{bad_jsonld} JSON-LD block(s) are not valid JSON")

    return out


def render_text(result):
    i = result["info"]
    print(f"URL: {result['input_url']}")
    if i.get("final_url"):
        print(f"Final: {i.get('final_url')}  Status: {i.get('status')}")
    print(f"Title: {i.get('title', '')!r}")
    print(f"Description: {i.get('meta_description', '')!r}")
    print(f"Canonical(s): {i.get('canonicals', [])}")
    print(f"H1: {i.get('h1', [])}")
    print(f"Links: internal={i.get('internal_links', 0)} external={i.get('external_links', 0)}")
    print(f"Images: {i.get('images', 0)} missing-alt-attr={i.get('images_missing_alt_attribute', 0)}")
    print(f"JSON-LD types: {i.get('jsonld_types', [])}")
    for e in result["errors"]:
        print(f"ERROR: {e}")
    for w in result["warnings"]:
        print(f"WARN: {w}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = scan(args.url)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        render_text(result)
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
