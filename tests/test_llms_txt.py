import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "seo" / "scripts"))
import llms_txt  # noqa: E402


class LlmsTxtTests(unittest.TestCase):
    def test_render_skips_noindex(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "index.html").write_text('<title>Home</title><meta name="description" content="Welcome">')
            (root / "hidden.html").write_text('<title>Hidden</title><meta name="robots" content="noindex">')
            out = llms_txt.render(llms_txt.collect(root), "https://e.invalid/", "Example", "Sum")
        self.assertIn("# Example", out)
        self.assertIn("- [Home](https://e.invalid/): Welcome", out)
        self.assertNotIn("Hidden", out)


if __name__ == "__main__":
    unittest.main()
