import json
import time
import random
from playwright.sync_api import sync_playwright

def run_crawler():
    # 1. Start Playwright and run it headless
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Emulate a standard desktop browser user agent
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page() # for isolated, private browsing session

        start_url = "https://www.kapruka.com/?utm_source=googleads&utm_medium=pxtm&gad_source=1&gad_campaignid=22913451767&gbraid=0AAAAAD_wZ62eBxT1XGypqg4kuAtiKXPbw&gclid=Cj0KCQjwzqXQBhD2ARIsAKrIeU93HyhweXvOggYxWRpG7p8dbGdXUfro2j0YnPToy7o1c08gfD7tjh4aAlxBEALw_wcB"  # Replace with your target
        all_products = []
        current_page_url = start_url
        category_links = set()
        
        max_pages = 3  # Safety limit for testing
        page_count = 1

        print("🚀 Starting crawler...")

        try:
            # --- STEP 1: Take product categories into a list from kapruka homepage ---   
            print(f"📸 Scraping Product categories from home page")
            page.goto(current_page_url, wait_until="domcontentloaded")

            # Wait for product cards to load (adjust selector to match your site)
            try:
                page.wait_for_selector(".rebrandCircles", timeout=5000)
            except Exception:
                print("⚠️ Timing out waiting for product cards, attempting to scrape anyway.")

            # Extract product links using JS evaluation
            links = page.eval_on_selector_all(
                ".rebrandCircles a", 
                "anchors => anchors.map(a => a.href)"
            )
            
            for link in links:
                category_links.add(link)
            print(f"🔗 Found {len(category_links)} Categories")


            category_page = context.new_page()

            for category in category_links:    
                category_name = category.split("/")[-1]
                print(f"Category name {category_name}\n")

                # verifying category url is valid and exist
                try:
                    category_page.goto(category, wait_until="domcontentloaded")
                except:
                    print(f"Category does not exist {category}")

                # page.goto(category, wait_until="domcontentloaded")

                # Look for the "Next" button pagination link
                # next_button = page.query_selector("a.next-page")
                # if next_button:
                #     next_url = next_button.get_attribute("href")
                #     # Construct absolute URL if the path is relative
                #     if next_url and not next_url.startswith("http"):
                #         from urllib.parse import urljoin
                #         current_page_url = urljoin(start_url, next_url)
                #     else:
                #         current_page_url = next_url
                #     page_count += 1
                # else:
                #     current_page_url = None

            # print(f"\n✅ Discovery complete. Found {len(product_links)} unique product URLs.")

            # --- STEP 2: DETAIL EXTRACTION ---
            # for url in product_links:
            #     print(f"🕵️‍♂️ Extracting data from: {url}")
            #     try:
            #         page.goto(url, wait_until="domcontentloaded")
            #         page.wait_for_selector(".product-title", timeout=5000)

            #         # Extract the details from the product page
            #         product_data = page.evaluate("""() => {
            #             const title = document.querySelector('.product-title')?.innerText.trim() || null;
            #             const price = document.querySelector('.product-price')?.innerText.trim() || null;
            #             const sku = document.querySelector('.product-sku')?.innerText.trim() || null;
            #             const availability = document.querySelector('.stock-status')?.innerText.trim() || 'In Stock';
                        
            #             return { title, price, sku, availability };
            #         }""")

            #         # Append metadata
            #         product_data["url"] = url
            #         product_data["scraped_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    
            #         all_products.append(product_data)
                    
            #         # Polite scraping: anti-ban sleep delay
            #         time.sleep(random.uniform(1.0, 2.5))

            #     except Exception as e:
            #         print(f"❌ Failed to scrape {url}: {e}")

            # --- STEP 3: SAVE TO JSON ---
            # with open("products.json", "w", encoding="utf-8") as f:
            #     json.dump(all_products, f, indent=4, ensure_ascii=False)
            
            # print(f"\n🎉 Done! Successfully saved {len(all_products)} items to products.json")

        finally:
            browser.close()

if __name__ == "__main__":
    run_crawler()