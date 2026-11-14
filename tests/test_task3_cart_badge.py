import pytest
from playwright.sync_api import Page, expect


@pytest.mark.parametrize(
    "products, expected_count",
    [
        (["Sauce Labs Backpack"], "1"),
        (["Sauce Labs Backpack", "Sauce Labs Bike Light"], "2"),
        (["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"], "3"),
    ],
)
def test_cart_badge(logged_in_page: Page, products: list[str], expected_count: str):
    page = logged_in_page
    for product in products:
        card = page.locator('[data-test="inventory-item"]').filter(has_text=product)
        card.get_by_role("button", name="Add to cart").click()

    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text(expected_count)
