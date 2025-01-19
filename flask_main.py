import asyncio
from flask import Flask, render_template, request
from playwright.async_api import async_playwright

app = Flask(__name__)

async def extract_reviews(url: str) -> dict:
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

        result = {
            "html_content": page_html,
            "reviews_count": None
        }

        # Try to extract the reviews count
        try:
            # Update this locator according to your page structure for review count
            review_count_locator = page.locator('span.review-count, .review-count, [aria-label*="reviews"], .reviews-count')

            # Extract the review count text
            reviews_count = await review_count_locator.text_content()
            result["reviews_count"] = reviews_count.strip() if reviews_count else "Not found"
        except Exception as e:
            result["reviews_count"] = f"Error extracting reviews count: {e}"

        # Close the browser
        await browser.close()

        return result


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            try:
                result = asyncio.run(extract_reviews(url))

                # Pass the result to the HTML template
                return render_template("index.html", result=result, url=url)
            except Exception as e:
                return render_template("index.html", error=f"An error occurred: {e}")
        else:
            return render_template("index.html", error="Please provide a URL.")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
