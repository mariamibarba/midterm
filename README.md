პაიჩარმის მომზადება: 

1.uv init - ხანდახან არ ეშვება და დაიკიდე

2.uv run playwright install chromium    

3.ბიბლიოთეკების დამატება - uv add pytest pytest-playwright pytest-html
4.uv run pytest -v --html=report.html --self-contained-html   -  გაუშვებს ყველა ტესტს და რეპორტში ჩაყრის
5. ბრაუზერში რომ ნახო როგორ ეშვება ტესტი  - uv run pytest tests/აქ შენი ფაილის სახელი ჩაწერე -v --headed --slowmo 1000

6.npx playwright codegen - კოდის გენერაცია

ფაილების სტრუქტურა - პროექტში შექმენი დირექტორია რონმელსაც დაარქმევ tests,  მერე დადექი ტესტზე და მანდ შექმენი ახალი დირექტორია pages. -  თუ ბონუს დავალების დაწერას აპირებ თუარადა tests - იც საკმარისია.







ნაბიჯი 1

from playwright.sync_api import Page, expect
 
 
def test_checkboxes(page: Page):
    page.goto("https://practice.expandtesting.com/checkboxes")
    checkbox1 = page.locator("#checkbox1")
    checkbox2 = page.locator("#checkbox2")
 
    # საწყისი მდგომარეობა
    expect(checkbox1).not_to_be_checked()
    expect(checkbox2).to_be_checked()
 
    # მონიშვნა / მოხსნა
    checkbox1.check()
    checkbox2.uncheck()
 
    expect(checkbox1).to_be_checked()
    expect(checkbox2).not_to_be_checked()


შემოწმება - uv run pytest tests/test_task1_checkboxes.py -v
ნაბიჯი 2:

import pytest
from playwright.sync_api import Page, expect
 
 
@pytest.mark.parametrize(
    "key, expected",
    [
        ("Escape", "You entered: ESCAPE"),
        ("a", "You entered: A"),
    ],
)
def test_key_presses(page: Page, key: str, expected: str):
    page.goto("https://practice.expandtesting.com/key-presses")
    page.locator("#target").press(key)
    expect(page.locator("#result")).to_have_text(expected)


ნაბიჯი 3:

import pytest
from playwright.sync_api import Page
 
SAUCE_URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
 
 
@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """შესვლა saucedemo-ზე და შესული გვერდის დაბრუნება."""
    page.goto(SAUCE_URL)
    page.locator("#user-name").fill(USERNAME)
    page.locator("#password").fill(PASSWORD)
    page.locator("#login-button").click()
    page.wait_for_url("**/inventory.html")
    return page


ნაბიჯი 4
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


ნაბიჯი 5:
import re
 
import pytest
from playwright.sync_api import Page, expect
 
URL = "https://demoqa.com/browser-windows"
 
 
@pytest.mark.parametrize("button_name", ["New Tab", "New Window"])
def test_new_tab_and_window(page: Page, button_name: str):
    page.goto(URL)
 
    with page.expect_popup() as info:
        page.get_by_role("button", name=button_name, exact=True).click()
    new_page = info.value
    new_page.wait_for_load_state()
 
    expect(new_page).to_have_url(re.compile(r"/sample$"))
    expect(new_page.locator("#sampleHeading")).to_have_text("This is a sample page")
 
    new_page.close()
    expect(page).to_have_url(URL)


ნაბიჯი 6 · Page Object-ები (Optional, დავალება 5)
tests/pages/login_page.py
from playwright.sync_api import Page, expect
 
 
class LoginPage:
    URL = "https://www.saucedemo.com/"
 
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
 
    def open(self):
        self.page.goto(self.URL)
 
    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
 
    def expect_loaded(self):
        expect(self.page).to_have_url(self.URL)
        expect(self.login_button).to_be_visible()
---------------------------------
tests/pages/inventory_page.py


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
-------------------
tests/pages/cart_page.py
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


ნაბიჯი 7 · tests/test_task5_cart_pom.py


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










ნაბიჯი 9 ·
commands.txt
პროექტის საქაღალდეში შექმენი
commands.txt
:
# 1. პროექტის შექმნა (PyCharm-მა გააკეთა uv-ით)
uv init
 
# 2. ბიბლიოთეკების დამატება
uv add pytest pytest-playwright pytest-html
 
# 3. ბრაუზერის ინსტალაცია
uv run playwright install chromium
 
# 4. ყველა ტესტის გაშვება და HTML რეპორტის შექმნა
uv run pytest -v --html=report.html --self-contained-html
 





