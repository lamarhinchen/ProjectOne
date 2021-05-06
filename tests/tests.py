import unittest
from psycopg2 import Error
from cust_exceptions.acct_already_exists import AcctAlreadyExists
from cust_exceptions.acct_does_not_exist import AcctDoesNotExist
from cust_exceptions.app_not_completed import AppNotCompleted
from cust_exceptions.incorrect_money_value import IncorrectMoneyValue
from cust_exceptions.invalid_value import InvalidValue
from dao.dao_imp import TuitionDao as TDTest
from services.tuition_service import TuitionService as STest


# ########################## TESTS ##############################################################
class TestMethods(unittest.TestCase):

    # Return all employees should be more than 1
    def test_all_employees_1(self):
        out = TDTest.get_emps()
        # Test more than one value is returned
        assert len(out[0]) > 0

    # Return 1 employee by ID
    def test_one_employee_1(self):
        out = TDTest.get_emps(1)
        # Test only one employee was returned
        assert len(out) == 1

    # Catch bad employee ID
    def test_one_employee_2(self):
        try:
            TDTest.get_emps("fdgdf")
            # Test a bad value was submitted
            raise AssertionError("You didn't catch the bad data put in for an ID!")
        except ValueError as e:
            assert e

    # Catch bad employee ID at the service level
    def test_one_employee_3(self):
        try:
            STest.get_employee_by_id("fdgdf")
            # Test a bad value was submitted
            raise AssertionError("You didn't catch the bad data put in for an ID!")
        except ValueError as e:
            assert e

    # Employee does not exist
    def test_one_employee_4(self):
        try:
            employee = 5634
            STest.get_employee_by_id(employee)
            # Test a bad value was submitted
            raise AssertionError("This employee does not exist!")
        except AcctDoesNotExist as e:
            assert e.message == f"empID: {employee} does not exist!"

    # Test app submission completes without optional data
    def test_optional_app_data_1(self):
        # No second address, sup approval, sup_approval_attach, or dept approval provided
        sub_app = {
            "address": "1165 stevens st.",
            "city": "new york",
            "state": "new york",
            "zip": 18595,
            "description": "It is an accounting course to obtain my Masters of accounting.",
            "work_just": "It would advance my ability to do my job.",
            "price_tag": 400.00,
            "event_types": "courses",
            "grade_format": "grade",
            "missed_time": 100,
            "date_event": "09/15/2021"
        }
        out = STest.submit_app(6, sub_app)
        # Test app should still go through without optional data
        assert len(out) == 1

    # Test app submission completes with optional data and supervisor approval is attached
    def test_optional_app_data_2(self):
        # Checking that the sup approval is true when supervisor approval is attached
        sub_app = {
            "address": "1165 stevens st.",
            "address_second": "apt 1511",
            "city": "new york",
            "state": "new york",
            "zip": 18595,
            "description": "It is an accounting course to obtain my Masters of accounting.",
            "work_just": "It would advance my ability to do my job.",
            "price_tag": 400.00,
            "event_types": "courses",
            "grade_format": "grade",
            "sup_approval_attach": "True",
            "sup_approval": "null",
            "dept_approval": "null",
            "missed_time": 100,
            "date_event": "09/15/2021"
        }
        out = STest.submit_app(6, sub_app)
        # Test output should show that since the supervisor approval is attached sup_approval is true
        assert len(out) == 1

    # Test app submission completes with optional data and supervisor approval is not attached
    def test_optional_app_data_3(self):
        # Checking that the sup approval is false when supervisor approval is not attached
        sub_app = {
            "address": "1165 stevens st.",
            "address_second": "apt 1511",
            "city": "new york",
            "state": "new york",
            "zip": 18595,
            "description": "It is an accounting course to obtain my Masters of accounting.",
            "work_just": "It would advance my ability to do my job.",
            "price_tag": 400.00,
            "event_types": "courses",
            "grade_format": "grade",
            "sup_approval_attach": "False",
            "sup_approval": "null",
            "dept_approval": "null",
            "missed_time": 100,
            "date_event": "09/15/2021"
        }
        out = STest.submit_app(6, sub_app)
        # Test output should show that since the supervisor approval is attached sup_approval is false
        assert out[0]['Supervisor Attached Approval'] is False

    # Test app won't go through if the ID does not exist
    def test_bad_app_id_data_1(self):
        try:
            employee = 2564
            # No address is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(employee, sub_app)
            raise AssertionError("Employee ID does not exist!")
        except AcctDoesNotExist as e:
            # Test Id does not exist
            assert e.message == f"empID: {employee} does not exist!"

    # Test app won't go through if the ID does not exist if sent as a string
    def test_bad_app_id_data_2(self):
        try:
            employee = "2564"
            # No address is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(employee, sub_app)
            raise AssertionError("Employee ID does not exist!")
        except AcctDoesNotExist as e:
            # Test Id does not exist as a string
            assert e.message == f"empID: {employee} does not exist!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_1(self):
        try:
            # No address is provided
            sub_app = {
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(6, sub_app)
            raise AssertionError("Address is missing!")
        except AppNotCompleted as e:
            # Test missing address was caught
            assert e.message == "Please fill in your address!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_2(self):
        try:
            # No city is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("City is missing!")
        except AppNotCompleted as e:
            # Test missing city was caught
            assert e.message == "Please provide your city!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_3(self):
        try:
            # No state is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("State is missing!")
        except AppNotCompleted as e:
            # Test missing state was caught
            assert e.message == "Please provide your state!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_4(self):
        try:
            # No zip is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("Zip is missing!")
        except AppNotCompleted as e:
            # Test missing zip was caught
            assert e.message == "Please provide your zip!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_5(self):
        try:
            # No description is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("Description is missing!")
        except AppNotCompleted as e:
            # Test missing description was caught
            assert e.message == "Please give a description or the curriculum!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_6(self):
        try:
            # No work justification is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("Work Justification is missing!")
        except AppNotCompleted as e:
            # Test missing work justification was caught
            assert e.message == "Please provide a short description to justify the reason!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_7(self):
        try:
            # No total cost is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("Cost is missing!")
        except AppNotCompleted as e:
            # Test missing Cost was caught
            assert e.message == "Please provide the full cost!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_8(self):
        try:
            # No event type is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("Event type is missing!")
        except AppNotCompleted as e:
            # Test missing Event type was caught
            assert e.message == "Please provide what type of event it is!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_9(self):
        try:
            # No grade format is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "sup_approval": "null",
                "dept_approval": "null",
                "date_event": "09/15/2021"
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("Grade format is missing!")
        except AppNotCompleted as e:
            # Test missing grade format was caught
            assert e.message == "Please provide the grading format!"

    # Test app submission catches appropriate errors
    def test_missing_app_data_10(self):
        try:
            # No event date is provided
            sub_app = {
                "address": "1165 stevens st.",
                "address_second": "apt 1511",
                "city": "new york",
                "state": "new york",
                "zip": 18595,
                "description": "It is an accounting course to obtain my Masters of accounting.",
                "work_just": "It would advance my ability to do my job.",
                "price_tag": 400.00,
                "event_types": "courses",
                "grade_format": "grade",
                "sup_approval": "null",
                "dept_approval": "null",
            }
            STest.submit_app(3, sub_app)
            raise AssertionError("Event Date is missing!")
        except AppNotCompleted as e:
            # Test missing Event date was caught
            assert e.message == "Please provide the date of the event!"


if __name__ == '__main__':
    unittest.main()
