import random
from behave import *
from UI_XPaths.pages_homepage import *
from features.common_functions import *


@step('Launch "{browser_type}" browser')
def step_impl(context, browser_type):
    """
    This steps launches web browser of select browser type
    :param context: context of the run
    :param browser_type: 'Chrome', 'Firefox', 'Edge' etc.,
    :return: returns success message otherwise asserts False
    """
    try:
        launch_web_browser(context, browser_type)
        logging.info(f'Launched {browser_type} browser')
    except Exception as err:
        assert False, f'{err}'


@step('Navigate to Demo page')
def step_impl(context):
    """
    This step navigates to demo page
    :param context: context of the run
    :return: returns success message otherwise asserts False
    """
    try:
        url = 'https://react-shopping-cart-67954.firebaseapp.com/'
        # Navigating to demo page and verifying products are displayed with XPath
        status = open_url_and_verify_xpath_present(context, url, homepage['products_display'])
        if status:
            logging.info(f'Navigated to {url} successfully')
        else:
            assert False, f'Failed to navigate to {url}'
    except Exception as err:
        assert False, f'{err}'


@step('Refreshing the page')
def step_impl(context):
    """
    This step refreshes page and waits for 'Add to cart' button to appear so as to check if screen is loaded
    :param context: context of the run
    :return: returns success message otherwise asserts False
    """
    try:
        refresh_page_and_wait_for_xpath(context, homepage['products_display'])
        logging.info(f'Page refreshed')
    except Exception as err:
        assert False, f'{err}'


@step('I Select {size} filter(s) and check if product is displayed')
def select_size_filter(context, size: list):
    """
    This step helps to select single filter or multiple filters
    :param context: context of the run
    :param size: [S, M, XS] for multiple filters or [S] for single filter
    :return: returns success message otherwise asserts False
    """
    try:
        size = eval(size)
        response = get_products_list_over_api()
        products_list = response['products']
        for each_size in size:
            click_status = click_on_element_by_xpath(context, homepage['size'].replace('~', each_size), 10)
            if not click_status:
                assert False, f"Failed to select size - {size}"
            # time.sleep(2)
            logging.info(f'Clicked on Size - "{size}" successfully')

        prod_title_list = get_multiple_elements_text_by_xpath(context, product_details['product_title'])
        for each_size in size:
            if not [product['title'] for product in products_list if each_size in product['availableSizes'] and product['title'] in prod_title_list]:
                assert False, 'Failed! Products are not displayed as per the size set'
        logging.info(f'Success! Products displayed - {prod_title_list} as per the size - {size}')

    except Exception as err:
        assert False, f'{err}'


@step('Add "{num}" items "{with_or_without}" free shipping')
def add_items_to_cart(context, num: int, with_or_without: str):
    """
    This step is used to add to add items to cart
    :param context: context of the run
    :param num: Number of items to be added to cart
    :param with_or_without: Give 'With' to add item with free shipping or 'Without' to add item without free shipping
    :param repeat_same_product: Give a number to indicate how many times a product will be added to cart
    :param verify_order_of_items_in_cart: Give 'True' to verify items are listed in the order as added to cart
    :return:
    """
    try:
        response = get_products_list_over_api()
        products = response['products']
        repeat_products = 1
        verify_order_of_items_in_cart = False
        prod_names_list = []
        if context.table:
            for each_row in context.table:
                if each_row['Field'] == 'repeat_same_product':
                    repeat_products = each_row['Value']
                elif each_row['Field'] == 'verify_order_of_items_in_cart':
                    verify_order_of_items_in_cart = each_row['Value']

        # Initiating context variable
        click_status_1 = click_on_element_by_xpath(context, homepage['cart_button'])
        if not click_status_1:
            assert False, f'Failed to click on Cart button'
        elif len(get_multiple_elements_text_by_xpath(context, cart_tab['items_in_cart'])) == 0:
            context.prod_names = []
        # Closing cart window
        click_status_2 = click_on_element_by_xpath(context, homepage['cart_X_button'])
        if not click_status_2:
            assert False, f'Failed to click on "X" button to close cart window'

        if with_or_without.lower() == 'with':
            prods_list = [each_product for each_product in products if each_product['isFreeShipping']]
            logging.info(f'Products with free shipping - {prods_list}')
        else:
            prods_list = [each_product for each_product in products if not each_product['isFreeShipping']]
            logging.info(f'Products without free shipping - {prods_list}')
        for _ in range(int(num)):
            if len(prods_list) >= int(num):
                # Using random.randrange(1, 10) to click on products randomly
                product_name = prods_list[random.randrange(1, len(prods_list))]['title']
                for i in range(repeat_products):
                    click_status_3 = click_on_element_by_xpath(context, homepage['add_to_card_button']
                                                               .replace('~', product_name))
                    if not click_status_3:
                        assert False, f'Failed to click on "Add to cart" button for product - {product_name}'
                if product_name not in prod_names_list:
                    prod_names_list.append(product_name)
                # Closing cart window to click on products without any issue
                click_status_4 = click_on_element_by_xpath(context, homepage['cart_X_button'])
                if not click_status_4:
                    assert False, f'Failed to click on "X" button to close cart window'
                # time.sleep(3)
            else:
                assert False, f'Given number of items - {num} is more than the num of products - {len(prods_list)} ' \
                              f'available {with_or_without} free shipping'
        if not context.prod_names:
            context.prod_names = prod_names_list
        else:
            context.prod_names = context.prod_names + prod_names_list

        if verify_order_of_items_in_cart:
            click_status_5 = click_on_element_by_xpath(context, homepage['cart_button'])
            if not click_status_5:
                assert False, f'Failed to click on Cart button'
            list_of_items_in_cart = get_multiple_elements_text_by_xpath(context, cart_tab['items_in_cart'])
            # Closing cart window
            click_status_6 = click_on_element_by_xpath(context, homepage['cart_X_button'])
            if not click_status_6:
                assert False, f'Failed to click on "X" button to close cart window'
            elif list_of_items_in_cart == context.prod_names:
                logging.info("Success! Items are listed in the order as added to cart")
            else:
                assert False, 'Failed! Items are not listed in order as added to cart'

    except Exception as err:
        assert False, f'{err}'



