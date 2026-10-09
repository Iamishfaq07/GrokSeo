import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "seo" / "scripts"))
import build_scan  # noqa: E402


def page(title="T", desc="D", extra="", h1="<h1>H</h1>", canon=True):
    c = '<link rel="canonical" href="https://e.invalid/">' if canon else ""
    return (f'<html lang="en"><head><title>{title}</title><meta name="description" content="{desc}">{c}{extra}'
            f"</head><body>{h1}</body></html>")


class BuildScanTests(unittest.TestCase):
    def test_issues(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "index.html").write_text(page("Home", "Home page", h1="<h1>Home</h1><a href='/about/'>a</a><a href='/gone/'>g</a>"))
            (root / "about").mkdir()
            (root / "about" / "index.html").write_text(page("Home", "Other"))
            (root / "draft.html").write_text(page(extra='<meta name="robots" content="noindex">', canon=False))
            (root / "bare.html").write_text("<html><body>x</body></html>")
            res = build_scan.scan(root)["issues"]
        self.assertEqual(res["noindex"], ["/draft.html"])
        self.assertIn("/bare.html", res["missing_title"])
        self.assertTrue(any("/gone/" in x for x in res["broken_internal_link"]))
        self.assertFalse(any("/about/" in x for x in res["broken_internal_link"]))
        self.assertEqual(len(res["duplicate_title"]), 1)
        self.assertNotIn("/draft.html", res.get("missing_canonical", []))


if __name__ == "__main__":
    unittest.main()
