import asyncio

from logger import Log
from utils import take_screenshot

async def handle_cookie_consent(amazon):
    try:
        await amazon.cookie_reject_button.wait_for(state="visible", timeout=3000)
        await amazon.cookie_reject_button.click()
        await asyncio.sleep(2)  # Slowing down to reduce flakiness
        Log.info("Cookie consent declined.")
    except Exception:
        pass

async def handle_delivery_popup(amazon):
    try:
        await amazon.dismiss_button.wait_for(state="visible", timeout=3000)
        await amazon.dismiss_button.click()
        Log.info("Delivery location popup dismissed.")
    except Exception:
        pass

async def handle_popups(amazon):
    await handle_cookie_consent(amazon)
    await handle_delivery_popup(amazon)

async def perform_search(amazon, query):
    try:
        await amazon.search_box.wait_for(state="visible", timeout=10000)
        await amazon.search_box.fill(query)
        await amazon.search_button.wait_for(state="attached", timeout=5000)
        await amazon.search_button.click()
        Log.info(f"Searching for {query}...")
        return True
    except Exception as e:
        Log.error(f"Search failed: {e}")
        await take_screenshot(amazon.page, "search_fail")
        return False

async def verify_search_results_visible(amazon):
    try:
        await asyncio.wait_for(asyncio.gather(
            amazon.results_heading.wait_for(state="visible"),
            return_exceptions=True
        ), timeout=10000)
        Log.info("Search completed.")
        return True
    except asyncio.TimeoutError:
        try:
            await amazon.alt_results_text.wait_for(state="visible", timeout=5000)
            return True
        except Exception:
            await take_screenshot(amazon.page, "results_not_found")
            Log.error("Neither primary nor fallback result indicators appeared.")
            return False

# Supported sorting options
SORT_OPTIONS = {
    "price-high-to-low": "#s-result-sort-select_2",
    "price-low-to-high": "#s-result-sort-select_1",
}

async def sort_results(amazon, filter_key: str):
    selector = SORT_OPTIONS.get(filter_key)
    if not selector:
        Log.error(f"Unsupported sort filter: {filter_key}")
        return False
    try:
        await amazon.sort_dropdown.wait_for(state="attached", timeout=5000)
        await amazon.sort_dropdown.click()
        sort_option = amazon.page.locator(selector)
        await sort_option.wait_for(state="attached", timeout=3000)
        await sort_option.click()
        Log.info(f"Sorted results using filter: {filter_key}")
        return True
    except Exception as e:
        Log.error(f"Failed to sort results: {e}")
        await take_screenshot(amazon.page, "sort_fail")
        return False
    
async def open_product_by_index(amazon, index: int, debug: bool = False):
    try:
        product = amazon.get_nth_product(index - 1)
        await product.wait_for(state="visible", timeout=5000)
        if debug:
            await take_screenshot(amazon.page, f"search_results_product_list_{index}")
        Log.info(f"Clicking product at position {index}...")

        async with amazon.page.expect_navigation(wait_until="domcontentloaded"):
            await product.click()

        await asyncio.sleep(5)  # Content needs time to load
        Log.info(f"Opened product at position {index}.")
        if debug:
            await take_screenshot(amazon.page, f"opened_product_{index}")
        return True

    except Exception as e:
        Log.error(f"Product at position {index} not found or failed to open: {e}")
        await take_screenshot(amazon.page, f"debug/product_{index}_fail")
        return False
    
async def verify_product_title(amazon, expected_substring: str = "Nikon D3X"):
    try:
        await amazon.title_element.wait_for(state="visible", timeout=5000)
        title_text = (await amazon.title_element.inner_text()).strip()
        Log.info(f"Product title found: {title_text}")
        Log.info(f"Looking for text '{expected_substring}' (case-insensitive) in the title...")
        
        assert expected_substring.lower() in title_text.lower(), (
            f"Expected text '{expected_substring}' in the title not found"
        )
        Log.info(f"Expected text found. Title verification passed.")
        return True

    except AssertionError as ae:
        Log.error(f"Title assertion failed: {ae}")
        await take_screenshot(amazon.page, "title_assert_fail")
        return False

    except Exception as e:
        Log.error(f"Failed to verify product title: {e}")
        await take_screenshot(amazon.page, "title_error")
        return False
        