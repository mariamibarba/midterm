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
