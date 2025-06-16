import logging
from POM.home_page import HomePage
from POM.search_results_page import SearchResultsPage
import config
import test_data
import re


def test_product_search(test_driver):
    logger = logging.getLogger("test_product_search")
    logger.info("Starting product search test")

    home = HomePage(test_driver, logger)
    home.go_to_page(config.url)
    home.search_product(test_data.product_name)

    results = SearchResultsPage(test_driver, logger)
    results.apply_filters(test_data.brand, test_data.color, test_data.price)

    result_text = results.get_result_count_text()
    assert result_text != "", "Result count text not found"

    match = re.search(r"[\d,.]+", test_data.price)
    price_max = float(match.group().replace(',', '')) if match else float('inf')

    count = results.get_result_count()
    assert count > 0, "No products found after applying filters"

    assert results.check_products_brand_and_price(test_data.brand, test_data.max_price)

    logger.info("Product search test completed successfully")
