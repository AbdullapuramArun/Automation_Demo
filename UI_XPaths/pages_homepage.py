homepage = {
    "size": "//input[@value='~']/..//span",  # Replace ~ with size filter (XS, S, M, L..)
    "products_display": "//*[contains(@class,'hewZDo')]",
    "add_to_card_button": "//div[@alt='~']/..//button[contains(@class,'124al1g-0')]",  # Replace ~ with product title
    "cart_button": "//button[contains(@class,'1h98xa9-0')]",
    "cart_X_button": "//*[contains(@class,'1h98xa9-0')]/span",
    "spinner": "//*[contains(@class,'5z44op')]"
}

product_details = {
    "product_title": "//p[contains(@class,'124al1g-4')]",
    "product_cost": "//p[contains(@class,'124al1g-6')]"
}

cart_tab = {
    "cart_heading": "//span[contains(text(),'Cart')]",
    "items_in_cart": "//*[contains(@class,'elbkhN')]",
    "plus_button": "//button[contains(text(),'+')]",
    "remove_product_button": "//button[@title='remove product from cart']",
    "total_cost": "//p[contains(text(),'SUBTOTAL')]/..//p[contains(@class,'jzywDV')]",
    "checkout_button": "//button[@class='sc-1h98xa9-11 gnXVNU']"
}