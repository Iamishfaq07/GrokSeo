import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "seo" / "scripts"))
import seo_scan  # noqa: E402

GOOD = """<!doctype html><html lang="en"><head><title>Widgets | Acme</title>
<meta name="description" content="Buy widgets."><meta name="viewport" content="width=device-width">
<link rel="canonical" href="https://example.invalid/widgets">
<script type="application/ld+json">{"@type":"Organization","name":"Acme"}</script>
</head><body><h1>Widgets</h1> trailing text <h2>Sizes</h2><a href="/a">a</a><img src="x.png" alt="x"></body></html>"""

BAD = """<html><head><meta name="robots" content="noindex"><script type="application/ld+json">{bad</script></head>
<body><img src="x.png"></body></html>"""


def run(html):
    out = {"errors": [], "warnings": [], "info": {}}
    seo_scan.analyze(html, "https://example.invalid/widgets", {}, out)
    return out


class ScanTests(unittest.TestCase):
    def test_good_page(self):
        o = run(GOOD)
        self.assertEqual(o["errors"], [])
        self.assertEqual(o["info"]["h1"], ["Widgets"])  # trailing text must not leak into H1
        self.assertEqual(o["info"]["jsonld_types"], ["Organization"])
        self.assertEqual(o["warnings"], [])

    def test_bad_page(self):
        o = run(BAD)
        self.assertIn("Missing <title>", o["errors"])
        joined = " ".join(o["warnings"])
        for needle in ("noindex", "not valid JSON", "No H1", "viewport", "lang"):
            self.assertIn(needle, joined)
        self.assertEqual(o["info"]["images_missing_alt_attribute"], 1)

    def test_json_serializable(self):
        json.dumps(run(GOOD))


if __name__ == "__main__":
    unittest.main()
