import re
from playwright.sync_api import Page, expect, sync_playwright
def test_has_title(page: Page):
    page.goto("https://www.kapruka.com/?utm_source=googleads&utm_medium=pxtm&gad_source=1&gad_campaignid=22913451767&gbraid=0AAAAAD_wZ62eBxT1XGypqg4kuAtiKXPbw&gclid=Cj0KCQjwzqXQBhD2ARIsAKrIeU93HyhweXvOggYxWRpG7p8dbGdXUfro2j0YnPToy7o1c08gfD7tjh4aAlxBEALw_wcB")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Kapruka"))

def test_get_started_link(page: Page):
    page.goto("https://www.kapruka.com/?utm_source=googleads&utm_medium=pxtm&gad_source=1&gad_campaignid=22913451767&gbraid=0AAAAAD_wZ62eBxT1XGypqg4kuAtiKXPbw&gclid=Cj0KCQjwzqXQBhD2ARIsAKrIeU93HyhweXvOggYxWRpG7p8dbGdXUfro2j0YnPToy7o1c08gfD7tjh4aAlxBEALw_wcB")

    # Click the get started link.
    page.get_by_role("link", name="Fruits").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Fresh Fruit Baskets Online - Kapruka")).to_be_visible()