@AllTests

Feature: This Feature file tests size filter, Adding items to cart and checkout to complete order

  @Size_Filter_Validation
  Scenario: Verifying user is able to filter items using size filter options
    Given Launch "Chrome" browser
    When Navigate to Demo page
    Then I Select ['XS'] filter(s) and check if product is displayed
    And Refreshing the page
    Then I Select ['XS', 'ML'] filter(s) and check if product is displayed

  @Add_Items_to_cart
  Scenario: Verifying user can add items to cart
    Given Launch "Chrome" browser
    When Navigate to Demo page
    Then Add "4" items "with" free shipping
      | Field  | Value |
      | verify_order_of_items_in_cart | True |
    Then Add "1" items "without" free shipping
      | Field  | Value |
      | verify_order_of_items_in_cart | True |
