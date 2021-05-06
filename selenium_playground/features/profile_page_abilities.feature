Feature: While a User is on their profile Page they can view, approve, reject, and request more info for assigned tasks
  Management can View, Approve, Reject, and Request additional info per each assigned task

  @ViewApplication
    Scenario: Management Can View a Reimbursement Request
    Given I am on the Tuition Reimbursement Profile Page
    When I load the Page
    Then all work Assigned to me Loads

  @ApproveApplication
    Scenario: Management Can Approve a Reimbursement Request
    Given I am on the Tuition Reimbursement Profile Page
    When I load the Page all work Assigned to me Loads
    Then I can Approve a Application

  @RejectApplication
    Scenario: Management Can Reject a Reimbursement Request
    Given I am on the Tuition Reimbursement Profile Page
    When I load the Page all work Assigned to me Loads
    Then I can Reject an Application

  @RequestAdditionalInfoApplication
    Scenario: Management Can Request More Information from a Reimbursement Request
    Given I am on the Tuition Reimbursement Profile Page
    When I load the Page all work Assigned to me Loads
    Then I can request More Information a Application