Feature: Logging in on the Tuition Home Page
    Login to the correct Application Submission Page
    Login to the correct User Profile Page
    Complete Tasks that are routed to the User
    Login to your profile if you are a supervisor
    Login to your profile if you are a department head

@LoginTest

Scenario: Login to the correct Application Submission Page if you are a supervisor
    Given I am on the Tuition Reimbursement Home Page
    When I enter user email as bi in the Search Bar
    Then Dropdown of the search results should appear
    When I Click the link for the Email I am looking for
    Then It should route me to the correct User Profile Page

Scenario: Login to the correct Application Submission Page if you are a Department Head
    Given I am on the Tuition Reimbursement Home Page
    When I enter user email as lam in the Search Bar
    Then Dropdown of the search results should appear
    When I Click the link for the Email I am looking for
    Then It should route me to the correct dept head User Profile Page

Scenario: Enter an Email that does not exist in the system
    Given I am on the Tuition Reimbursement Home Page
    When I enter user email as jz in the Search Bar
    Then Dropdown of the search should show No employees with this email exist!
