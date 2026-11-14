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
