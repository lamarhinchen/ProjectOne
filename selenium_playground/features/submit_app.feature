Feature: Submitting a Reimbursement Application
  Login to Application to have it pre-fill your information
  Complete all required fields of the form
  Submit only when the form is complete
  @SubmitApplication
    Scenario: Application Login with correct user information
    Given I am on the Tuition Reimbursement Home Page
    When I type my email in the search bar
    Then My full email shows underneath as a link
    When I click the email link
    Then My First, Middle, and Last name Load into their respective fields

  @SubmitApplication
  Scenario: Login to the Application Submission Page even if you are a supervisor
    Given I am on the Tuition Reimbursement Application Page
    When I try to submit the application before all required fields were completed
    Then Nothing happens
    When I complete the form correctly
    Then The submit button becomes enabled

  @ValueCorrection
  Scenario Outline: The form auto corrects bad input values
    Given I am on the Tuition Reimbursement Application Page
    When I input a negative value in a number field
    Then The field should auto correct itself to one
    Examples: Cost
      | -1        | 1     |
      | 111111    | 99999 |
      | 999999.99 | 99999 |