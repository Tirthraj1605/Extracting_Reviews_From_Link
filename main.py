import asyncio
from playwright.async_api import async_playwright

async def extract_reviews(url: str) -> None:
    """
    Extract reviews and their count from the given URL.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)

        # Get the HTML content of the page
        page_html = await page.content()
        print("HTML Content:")
        print(page_html)

        # Now, try to extract the reviews count
        try:
            # Update this locator according to your page structure for review count
            review_count_locator = page.locator('span.review-count, .review-count, [aria-label*="reviews"], .reviews-count')

            # Use locator's text_content() to get the review count
            reviews_count = await review_count_locator.text_content()
            print(f"Reviews Count: {reviews_count}")
            
        except Exception as e:
            print(f"An error occurred while extracting review count: {e}")

        # Close browser
        await browser.close()

# Main Function for Testing
if __name__ == "__main__":
    url = input("Enter the product page URL: ")
    try:
        asyncio.run(extract_reviews(url))
    except Exception as e:
        print(f"An error occurred: {e}")
