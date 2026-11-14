from playwright.sync_api import Page, expect


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def add_to_cart(self, product_name: str):
        card = self.page.locator('[data-test="inventory-item"]').filter(has_text=product_name)
        card.get_by_role("button", name="Add to cart").click()

    def open_cart(self):
        self.cart_link.click()

    def logout(self):
        self.menu_button.click()
        self.logout_link.click()

    def expect_loaded(self):
        expect(self.page).to_have_url(self.URL)
        expect(self.title).to_have_text("Products")

    def expect_badge(self, count: str):
        expect(self.cart_badge).to_have_text(count)
