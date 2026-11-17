"""Page Object Model for the local demo storefront."""
from playwright.sync_api import Page, expect


class StorePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self):
        self.page.goto(self.base_url, wait_until="networkidle")
        expect(self.page.get_by_role("heading", name="Retail Demo Store")).to_be_visible()
        return self

    def search(self, term: str):
        self.page.get_by_role("searchbox", name="Search products").fill(term)
        return self

    def add(self, product: str):
        self.page.get_by_role("button", name=f"Add {product} to cart").click()
        return self

    def count(self, expected: int):
        expect(self.page.locator("#cart-count")).to_have_text(str(expected))
        return self

    def total(self, expected: str):
        expect(self.page.locator("#cart-total")).to_have_text(expected)
        return self

    def increase(self, product: str):
        self.page.get_by_role("button", name=f"Increase {product}").click()
        return self

    def decrease(self, product: str):
        self.page.get_by_role("button", name=f"Decrease {product}").click()
        return self

    def checkout(self, name: str, email: str):
        self.page.get_by_role("textbox", name="Full name").fill(name)
        self.page.get_by_role("textbox", name="Email").fill(email)
        self.page.get_by_role("button", name="Place demo order").click()
        return self

    def message(self, text: str):
        expect(self.page.locator("#feedback")).to_contain_text(text)
        return self
