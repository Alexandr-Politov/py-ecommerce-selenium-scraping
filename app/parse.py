import csv
from dataclasses import dataclass, fields, astuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://webscraper.io/"
HOME_URL = urljoin(BASE_URL, "test-sites/e-commerce/more/")

COMPUTERS_URL = urljoin(HOME_URL, "computers/")
LAPTOPS_URL = urljoin(COMPUTERS_URL, "laptops/")
TABLETS_URL = urljoin(COMPUTERS_URL, "tablets/")

PHONES_URL = urljoin(HOME_URL, "phones/")
TOUCH_URL = urljoin(PHONES_URL, "touch/")

HOME_PAGE_CSV_PATH = "home.csv"
COMPUTERS_CSC_PATH = "computers.csv"
LAPTOPS_CSC_PATH = "laptops.csv"
TABLETS_CSC_PATH = "tablets.csv"
PHONES_CSC_PATH = "phones.csv"
TOUCH_CSC_PATH = "touch.csv"


@dataclass
class Product:
    title: str
    description: str
    price: float
    rating: int
    num_of_reviews: int

PRODUCT_FIELDS = [field.name for field in fields(Product)]


def parse_single_product(product_soup: BeautifulSoup) -> Product:
    return Product(
        title=product_soup.select_one("a.title")["title"],
        description=product_soup.select_one("p.description.card-text").text,
        price=float(product_soup.select_one("h4.price").text[1:]),
        rating=int(product_soup.select_one("p[data-rating]")["data-rating"]),
        num_of_reviews=int(product_soup.select_one("p.review-count.float-end")
                           .text.split()[0])
    )


def click_more_button(product_soup: BeautifulSoup) -> None: #TODO using selenium
    pass


def get_all_products_from_site_section(url: str) -> [Product]:
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")

    products = soup.select(".card.thumbnail")

    return (parse_single_product(product_soup) for product_soup in products)


def write_products_to_csv(products: [Product], file_path: str) -> None:
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(PRODUCT_FIELDS)
        writer.writerows([astuple(prod) for prod in products])


def main() -> None:
    home_products = get_all_products_from_site_section(HOME_URL)
    write_products_to_csv(home_products, HOME_PAGE_CSV_PATH)

    computers_products = get_all_products_from_site_section(COMPUTERS_URL)
    write_products_to_csv(computers_products, COMPUTERS_CSC_PATH)

    laptops_products = get_all_products_from_site_section(LAPTOPS_URL)
    write_products_to_csv(laptops_products, LAPTOPS_CSC_PATH)

    tablets_products = get_all_products_from_site_section(TABLETS_URL)
    write_products_to_csv(tablets_products, TABLETS_CSC_PATH)

    phones_products = get_all_products_from_site_section(PHONES_URL)
    write_products_to_csv(phones_products, PHONES_CSC_PATH)

    touch_products = get_all_products_from_site_section(TOUCH_URL)
    write_products_to_csv(touch_products, TOUCH_CSC_PATH)


if __name__ == "__main__":
    main()
