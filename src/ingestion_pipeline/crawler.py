import json
import time
import random
from playwright.sync_api import sync_playwright
import json

def run_crawler():
    # 1. Start Playwright and run it headless
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Emulate a standard desktop browser user agent for isolated, private browsing session
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        home_page = context.new_page()

        start_url = "https://www.kapruka.com/?utm_source=googleads&utm_medium=pxtm&gad_source=1&gad_campaignid=22913451767&gbraid=0AAAAAD_wZ62eBxT1XGypqg4kuAtiKXPbw&gclid=Cj0KCQjwzqXQBhD2ARIsAKrIeU93HyhweXvOggYxWRpG7p8dbGdXUfro2j0YnPToy7o1c08gfD7tjh4aAlxBEALw_wcB"  # Replace with your target
        category_links = set()

        print("🚀 Starting crawler...")

        try:
            # --- STEP 1: Take product categories into a list from kapruka homepage ---   
            print(f"📸 Scraping Product categories from home page")
            home_page.goto(start_url, wait_until="domcontentloaded")

            # Wait for product cards to load (adjust selector to match your site)
            try:
                home_page.wait_for_selector(".rebrandCircles", timeout=5000)
            except Exception:
                print("⚠️ Timing out waiting for product cards, attempting to scrape anyway.")

            # Extract product links using JS evaluation
            links = home_page.eval_on_selector_all(
                ".rebrandCircles a", 
                "anchors => anchors.map(a => a.href)"
            )
            
            for link in links:
                category_links.add(link)
            print(f"🔗 Found {len(category_links)} Categories")


            category_page = context.new_page()

            testing_category_link = next(iter(category_links))
            testing_cat_name = testing_category_link.split("/")[-1]
            print(f"Testing category is {testing_cat_name}")

            category_page.goto(testing_category_link, wait_until="domcontentloaded")
            print(f"Get into {testing_cat_name} Category")

            products_links = category_page.locator(".catalogueV2Repeater a")
            count = products_links.count()
            if count == 0:
                print("No products found on this page. Stopping.")

            product_urls = []

            for i in range(count):
                url = products_links.nth(i).get_attribute("href")

                if url:
                    # Make sure it's a full URL if the site uses relative paths
                    full_url = url if url.startswith("http") else f"{start_url}{url}"
                    if full_url not in product_urls:
                        product_urls.append(full_url)

            # Scrape Individual Product ---
            # Create a new tab/page to scrape details so we don't lose our place
            detail_page = context.new_page()

            json_data = {}

            if testing_cat_name not in json_data:
                json_data[testing_cat_name] = {}

            for url in product_urls:
                print(f"Scraping details from: {url}")
                try:
                    detail_page.goto(url, wait_until="domcontentloaded")
                    
                    # Pull the data (using selectors from our previous step)
                    name = detail_page.locator(".blockDelivery.imgtags h1").inner_text(timeout=3000)
                    price = detail_page.locator(".price .priceM").inner_text(timeout=3000)
                    desc = detail_page.locator(".detailDescription").inner_text(timeout=3000)
                    stock = detail_page.locator(".tagArea .tags", has_text="In Stock").inner_text()
                    
                    print(f"[SUCCESS] {name} | {price} | {stock}")

                    json_data[testing_cat_name][name] = {
                        "price": price,
                        "in stock": stock,
                        "description": desc
                    }
                    
                    # Here you would typically save this to a CSV or Database
                    
                except Exception as e:
                    print(f"[ERROR] Failed to scrape {url}: {e}")
                
                time.sleep(1) # Be a good internet citizen

            with open("products.json", "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)



        finally:
            browser.close()

if __name__ == "__main__":
    run_crawler()