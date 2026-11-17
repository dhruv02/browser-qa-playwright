"""Session-scoped local web server and isolated Chromium browser contexts.

PLAYWRIGHT_CHROMIUM_EXECUTABLE can point to an existing Chrome/Chromium
installation for environments where Playwright-managed binaries are unavailable.
"""
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from playwright.sync_api import sync_playwright

DEMO_ROOT = Path(__file__).resolve().parents[1] / "demo_store"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass


@pytest.fixture(scope="session")
def base_url():
    handler = partial(QuietHandler, directory=str(DEMO_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as playwright:
        options = {"headless": True}
        if os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE"):
            options["executable_path"] = os.environ["PLAYWRIGHT_CHROMIUM_EXECUTABLE"]
        browser = playwright.chromium.launch(**options)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def page(browser_instance, request):
    context = browser_instance.new_context(viewport={"width": 1366, "height": 850})
    tab = context.new_page()
    yield tab
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        output_dir = Path("test-results")
        output_dir.mkdir(exist_ok=True)
        tab.screenshot(path=str(output_dir / f"{request.node.name}.png"))
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        item.rep_call = report
