from playwright.sync_api import Page

from tests.pages.cart_page import CartPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.login_page import LoginPage

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]


def test_cart_with_page_objects(page: Page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    # 1. შესვლა და 3 პროდუქტის დამატება
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    for product in PRODUCTS:
        inventory_page.add_to_cart(product)
    inventory_page.expect_badge("3")

    # 2. კალათა → 3 პროდუქტი
    inventory_page.open_cart()
    cart_page.expect_item_count(3)

    # 3. Bike Light-ის წაშლა
    cart_page.remove("Sauce Labs Bike Light")
    cart_page.expect_items(["Sauce Labs Backpack", "Sauce Labs Onesie"])
    cart_page.expect_badge("2")

    # 4. Continue Shopping
    cart_page.continue_shopping()
    inventory_page.expect_loaded()

    # 5. Logout
    inventory_page.logout()
    login_page.expect_loaded()
