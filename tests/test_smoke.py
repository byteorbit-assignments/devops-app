from django.test import TestCase


URLS_PUBLIC = [
    "/",
]


class SmokeTests(TestCase):
    def test_public_urls(self):
        for url in URLS_PUBLIC:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
