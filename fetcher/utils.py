from pathlib import Path

import bs4
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}


def fetch_html(url: str, html_file: Path) -> str:
    print(f"Fetching HTML from {url}")

    html_doc = requests.get(
        url,
        headers=HEADERS,
    )

    if html_doc.status_code != 200:
        raise Exception("Failed to fetch HTML content")

    html_file.write_text(html_doc.text)

    return html_doc.text


def mix_soup(html: str):
    s = bs4.BeautifulSoup(html, "html.parser")
    return s.find_all("li", class_="product")


def morph_to_int(price) -> float:
    if price == "999999.00":
        return 0
    try:
        return int(
            price.replace(",", "").replace("$", "").replace("£", "").replace(".", "")
        )
    except ValueError:
        return 0


def check_availability(product_flags, price):
    if price == "999999.00":
        return "Unavailable"

    if product_flags:
        if isinstance(product_flags, str):
            if product_flags.startswith("000000"):
                return "Out of Stock"

    return "In Stock"


def process_products(products: list):
    col = {}
    for m_prod in products:
        ln_number = m_prod.find("span", class_="linkNo")

        col[ln_number.text] = {
            "ln_number": ln_number.text,
            "manufacturer": m_prod.attrs.get("data-manufacturer"),
            "description": m_prod.attrs.get("data-description")
            .replace("™", "")
            .replace("/", ""),
            "price": morph_to_int(m_prod.attrs.get("data-price")),
            "availability": check_availability(
                m_prod.attrs.get("data-productflags"), m_prod.attrs.get("data-price")
            ),
        }

    return col


def filter_new_in_stock(collection: dict) -> dict:
    processed: dict = {}

    for key, value in collection.items():
        if value["availability"] != "In Stock":
            continue

        if value["manufacturer"] in ["klevv", "Club 3D"]:
            continue

        if "Refurbished" in value["description"]:
            continue

        if "Bundle" in value["description"]:
            continue

        processed[key] = value

    return processed
