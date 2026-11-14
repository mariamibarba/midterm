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
