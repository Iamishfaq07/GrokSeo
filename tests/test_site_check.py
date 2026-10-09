import sys
import tempfile
import threading
import unittest
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "seo" / "scripts"))
import site_check  # noqa: E402


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


class ParseTests(unittest.TestCase):
    def test_parse_robots(self):
        sm, dis = site_check.parse_robots("User-agent: *\nDisallow: /\nSitemap: https://e.invalid/s.xml\n")
        self.assertEqual(sm, ["https://e.invalid/s.xml"])
        self.assertTrue(dis)
        self.assertFalse(site_check.parse_robots("User-agent: *\nDisallow: /cart/\n")[1])

    def test_parse_sitemap(self):
        self.assertEqual(site_check.parse_sitemap("<urlset><url><loc> https://e.invalid/a </loc></url></urlset>"),
                         (False, ["https://e.invalid/a"]))
        self.assertTrue(site_check.parse_sitemap("<sitemapindex><sitemap><loc>x</loc></sitemap></sitemapindex>")[0])


class LiveTests(unittest.TestCase):
    def serve(self, files):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        for name, body in files.items():
            (Path(d.name) / name).write_text(body)
        srv = HTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=d.name))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.server_close)
        self.addCleanup(srv.shutdown)
        return f"http://127.0.0.1:{srv.server_port}"

    def test_healthy_site(self):
        origin = self.serve({
            "index.html": "x",
            "robots.txt": "User-agent: *\nDisallow: /cart/\n",
            "sitemap.xml": "<urlset></urlset>",
        })
        res = site_check.check(origin)
        self.assertEqual(res["robots_status"], 200)
        self.assertEqual(res["issues"], [])
        self.assertEqual(res["sitemap_url_count"], 0)

    def test_missing_robots_and_bad_sitemap_url(self):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        srv = HTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=d.name))
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        self.addCleanup(srv.server_close)
        self.addCleanup(srv.shutdown)
        origin = f"http://127.0.0.1:{srv.server_port}"
        (Path(d.name) / "sitemap.xml").write_text(f"<urlset><url><loc>{origin}/missing</loc></url></urlset>")
        res = site_check.check(origin)
        text = " ".join(res["issues"])
        self.assertIn("robots.txt returned 404", text)
        self.assertIn("not 200", text)
        self.assertEqual(res["sitemap_non_200"][0]["status"], 404)

    def test_unreachable_origin_reports_one_issue(self):
        res = site_check.check("http://127.0.0.1:1")
        self.assertEqual(res["robots_status"], 0)
        self.assertEqual(len(res["issues"]), 1)
        self.assertIn("Could not connect", res["issues"][0])


if __name__ == "__main__":
    unittest.main()
