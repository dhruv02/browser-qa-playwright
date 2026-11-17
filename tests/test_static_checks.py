"""Fast smoke checks that don't require a Chromium browser installation."""
from pathlib import Path
from urllib.request import urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_demo_has_accessible_form_and_search():
    html = (PROJECT_ROOT / "demo_store" / "index.html").read_text(encoding="utf-8")
    assert '<html lang="en">' in html
    assert 'id="search" type="search"' in html
    assert '<label for="customer-email">Email</label>' in html
    assert 'id="checkout" novalidate' in html


def test_browser_tests_are_independent_of_external_services():
    js = (PROJECT_ROOT / "demo_store" / "store.js").read_text(encoding="utf-8")
    assert "localStorage" in js
    assert "fetch(" not in js
    assert "https://" not in js


def test_local_demo_server_delivers_html(base_url):
    with urlopen(base_url, timeout=5) as response:
        body = response.read().decode("utf-8")
        assert response.status == 200
        assert "Retail Demo Store" in body
