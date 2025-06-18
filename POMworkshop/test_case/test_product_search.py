import re
import logging

from POM.home_page import HomePage
from POM.search_page import SearchPage
import test_data
import config


def test_product_search(test_driver, test_logger):
    test_logger.info("Starting product search test")

    home = HomePage(test_driver, test_logger)
    home.go_to_page(config.url)
    home.search_product(test_data.product_name)

    search = SearchPage(test_driver, test_logger)
    search.apply_filters(test_data.brand, test_data.color, test_data.price)

    result_text = search.get_result_count_text()
    test_logger.info(f"Result count text found: '{result_text}'")
    assert result_text != "", "Result count text not found"

    # Parse max price dynamically from price string like "$200.00 and Under"
    match = re.search(r"[\d,.]+", test_data.price)
    price_max = float(match.group().replace(',', '')) if match else float('inf')
    test_logger.info(f"Parsed max price: {price_max}")

    count = search.get_result_count()
    test_logger.info(f"Number of products found after filters: {count}")
    assert count > 0, "No products found after applying filters"

    # brand_price_check = search.check_products_brand_and_price(test_data.brand, price_max)
    # assert brand_price_check, "One or more products do not match the expected brand or price"
