import argparse
import asyncio

from amazon_helpers import handle_popups, perform_search, verify_search_results, sort_results, open_product_by_index, verify_product_title
from elements import AmazonPage
from pathlib import Path
from playwright.async_api import async_playwright
from utils import normalize_url, navigate_to_url

# Default path to MS Edge on macOS
EDGE_PATH = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
# If tested on Windows, the path should look like: 
# EDGE_PATH = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

async def open_browser_with_url(
        url: str,
        search_term: str = "Nikon", 
        sort_filter: str = "price-high-to-low", 
        product_index: int = 2, 
        title_match: str = "Nikon D3X",
        debug_errors: bool = False
):
    edge_executable = Path(EDGE_PATH)
    if not edge_executable.exists():
        raise FileNotFoundError(f"Edge executable not found at {EDGE_PATH}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=EDGE_PATH, headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        print(f"Opening URL: {url}")
        if not await navigate_to_url(page, url):
            await browser.close()
            return

        if "amazon." in url:
            amazon = AmazonPage(page)
            await handle_popups(amazon)
            if not await perform_search(amazon, search_term):
                await browser.close()
                return
            if not await verify_search_results(amazon):
                await browser.close()
                return

            if not await sort_results(amazon, sort_filter):
                await browser.close()
                return

            if not await open_product_by_index(amazon, product_index, debug=debug_errors):
                await browser.close()
                return

            if not await verify_product_title(amazon, title_match):
                await browser.close()
                return
            
            print("Amazon search results analysis is finished.")

        await browser.close()

def main():
    parser = argparse.ArgumentParser(
        description="Automated Amazon search tester using Playwright.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("url", help="The URL to open in the Edge browser.")

    parser.add_argument(
        "--search",
        default="Nikon",
        help="Search term to use on Amazon (default: 'Nikon')"
    )
    parser.add_argument(
        "--filter",
        default="price-high-to-low",
        help="Sort filter: 'price-high-to-low' or 'price-low-to-high'"
    )
    parser.add_argument(
        "--index",
        type=int,
        default=2,
        help="Index of the product to open (1-based, starting from first actual result)"
    )
    parser.add_argument(
        "--title-match",
        default="Nikon D3X",
        help="Expected substring in the product title for validation"
    )

    parser.add_argument(
    "--debug",
    action="store_true",
    help="Print raw browser errors and get additional screenshots for debugging purposes"
)
    
    args = parser.parse_args()

    try:
        url = normalize_url(args.url)
    except ValueError as e:
        print(f"Error: {e}")
        return

    asyncio.run(open_browser_with_url(
        url, 
        args.search,
        args.filter, 
        args.index, 
        args.title_match,
        args.debug
    ))

if __name__ == "__main__":
    main()