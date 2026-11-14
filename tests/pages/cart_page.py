from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

    def remove(self, product_name: str):
        self.items.filter(has_text=product_name).get_by_role("button", name="Remove").click()

    def continue_shopping(self):
        self.continue_shopping_button.click()

    def expect_item_count(self, count: int):
        expect(self.items).to_have_count(count)

    def expect_items(self, names: list[str]):
        expect(self.item_names).to_have_text(names)

    def expect_badge(self, count: str):
        expect(self.cart_badge).to_have_text(count)
