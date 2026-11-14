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
