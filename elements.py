class AmazonPage:
    def __init__(self, page):
        # Main Page
        self.page = page
        self.dismiss_button = page.locator('input[data-action-type="DISMISS"]')
        self.cookie_reject_button = page.locator('#sp-cc-rejectall-link')
        self.search_box = page.locator('#twotabsearchtextbox')
        self.search_button = page.locator('#nav-search-submit-button')

        # Search Results Page
        self.results_heading = page.locator("h2:has-text('Results')")
        self.alt_results_text = page.locator("span:has-text('Check each product page')")
        self.sort_dropdown = page.locator('#a-autoid-0-announce')
        self.sort_price_desc = page.locator('#s-result-sort-select_2')
        self.second_product = page.locator('[data-component-type="s-search-result"][data-index="2"] a.a-link-normal')

        # Product Page
        self.title_element = page.locator('span#productTitle')

    def get_nth_product(self, index: int):
        product = self.page.locator('div[data-component-type="s-search-result"]').nth(index)
        return product.locator('a.a-link-normal').first
