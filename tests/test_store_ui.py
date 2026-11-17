"""End-to-end tests using role-based selectors and Page Object Model."""
import pytest
from playwright.sync_api import expect

from pages.store_page import StorePage


@pytest.fixture
def store(page, base_url):
    return StorePage(page, base_url).open()


def test_page_title_and_catalog(store):
    expect(store.page).to_have_title("Retail Demo Store | UI Automation Portfolio")
    expect(store.page.locator(".product")).to_have_count(4)


@pytest.mark.parametrize("term,expected", [
    ("Electronics", 2), ("NOTEBOOK", 1), ("not-a-product", 0), ("", 4)
])
def test_search_is_case_insensitive(store, term, expected):
    store.search(term)
    expect(store.page.locator(".product")).to_have_count(expected)
    expect(store.page.get_by_role("status").first).to_have_text(f"{expected} products found")


def test_add_to_cart_updates_totals(store):
    store.add("Wireless Mouse").count(1).total("$24.99")
    store.add("USB-C Cable").count(2).total("$37.49")


def test_repeated_items_and_remove(store):
    store.add("Notebook").increase("Notebook").count(2).total("$14.50")
    store.decrease("Notebook").count(1).total("$7.25")
    store.decrease("Notebook").count(0).total("$0.00")
    expect(store.page.get_by_text("Your cart is empty.")).to_be_visible()


def test_clear_cart(store):
    store.add("Desk Lamp").count(1)
    store.page.get_by_role("button", name="Clear cart").click()
    store.count(0).message("Cart cleared.")


def test_cannot_checkout_empty_cart(store):
    store.checkout("Test Customer", "test@example.com")
    store.message("Add at least one item before checkout.")


@pytest.mark.parametrize("name,email,message", [
    ("T", "test@example.com", "Enter your full name"),
    ("Tester", "invalid-email", "Enter a valid email address"),
    ("Tester", "", "Enter a valid email address"),
])
def test_checkout_validation(store, name, email, message):
    store.add("Notebook").checkout(name, email).message(message)
    store.count(1)


def test_valid_checkout_clears_cart(store):
    store.add("Desk Lamp").checkout("Jamie Tester", "jamie@example.com")
    store.message("Demo order placed for Jamie Tester: 1 item(s).")
    store.count(0).total("$0.00")


def test_cart_persists_after_page_reload(store):
    store.add("USB-C Cable")
    store.page.reload()
    store.count(1).total("$12.50")


def test_cart_is_isolated_between_browser_contexts(browser_instance, base_url):
    a = browser_instance.new_context()
    b = browser_instance.new_context()
    try:
        StorePage(a.new_page(), base_url).open().add("Notebook").count(1)
        StorePage(b.new_page(), base_url).open().count(0)
    finally:
        a.close()
        b.close()


def test_mobile_layout(page, base_url):
    page.set_viewport_size({"width": 375, "height": 812})
    store = StorePage(page, base_url).open()
    store.add("Notebook").count(1)
    expect(page.get_by_role("heading", name="Demo checkout")).to_be_visible()
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
