import re
from cust_exceptions.app_not_completed import AppNotCompleted
from cust_exceptions.invalid_value import InvalidValue
from dao.dao_imp import TuitionDao as TD


class TuitionService:

    # Submit a new application
    @classmethod
    def submit_app(cls, employee, sub_app):
        # Validate that the employee exists
        TD.get_emps(employee=employee)
        # Add the employeeID since they exist
        sub_app["emp_id"] = employee
        # Check if application is valid
        cls.validate_application(sub_app=sub_app)
        # Files the new application
        filed_app = TD.file_application(new_app=sub_app)
        # Gets the most current version of the application
        updated_app = TD.get_apps(app_data=filed_app[0].app_id)
        return [tuition_info.json() for tuition_info in updated_app.values()]

    # Get an employee by their ID
    @classmethod
    def get_employee_by_id(cls, employee):
        # Validate that the employee exists
        valid_emp = TD.get_emps(employee=employee)
        return valid_emp

    # Get an application by it's ID
    @classmethod
    def get_app(cls, app_data):
        # Validate that the application exists
        valid_app = TD.get_apps(app_data=app_data)
        return [tuition_info.json() for tuition_info in valid_app.values()]

    # Get the employee's supervisor by their ID
    @classmethod
    def get_sup_by_employee_id(cls, employee):
        # Validate that the employee exists
        TD.get_emps(employee=employee)
        # Find their supervisor
        valid_emp = TD.get_sup_by_emps(employee=employee)
        return [tuition_info.json() for tuition_info in valid_emp.values()]

    # Log the employee in
    @classmethod
    def employee_login(cls, employee):
        # Find the employee by email
        valid_emp = TD.get_emps_by_email(employee=employee)
        emp_login_info = [tuition_info.json() for tuition_info in valid_emp.values()]
        emp_login_info[0]["url"] = f"""http://localhost:5000/users/{emp_login_info[0]["Employee ID"]}"""
        return emp_login_info

    # Get all employees
    @classmethod
    def get_all_employees(cls):
        valid_emps = TD.get_emps()
        return valid_emps

    # Search a list of employees by email
    @classmethod
    def get_all_employees_search(cls, search_data=None):
        valid_emps = TD.search_emps_by_email(search_data)
        return [tuition_info.json() for tuition_info in valid_emps.values()]

    # Search for all the work that belongs to this employee
    @classmethod
    def get_employee_work(cls, employee=None):
        # Validate that the employee exists
        TD.get_emps(employee=employee)
        # Get all tasks assigned to employee
        valid_emps = TD.find_work(employee=employee)
        return [tuition_info.json() for tuition_info in valid_emps.values()]

    # Update an existing additional request
    @classmethod
    def update_add_info(cls, emp_id=None, info_id=None, up_req=None):
        # Validate that the employee exists
        TD.get_emps(employee=emp_id)
        # Validate that the additional info request exists
        TD.find_add_info_by_info_id(emp_id=emp_id, info_id=info_id)
        # Get all tasks assigned to employee
        valid_emps = TD.update_add_info(info_id=info_id, up_req=up_req)
        return [tuition_info.json() for tuition_info in valid_emps.values()]

    # Get all the applications an employee filed
    @classmethod
    def get_all_my_apps(cls, emp_id=None):
        # Validate that the employee exists
        TD.get_emps(employee=emp_id)
        # Get all the applications the employee filed
        valid_emps = TD.get_all_my_apps(emp_id=emp_id)
        return [tuition_info.json() for tuition_info in valid_emps.values()]

    # Create an additional info request
    @classmethod
    def make_add_info(cls, emp_id=None, to_emp_id=None, add_req=None):
        # Validate that the requesting employee exists
        TD.get_emps(employee=emp_id)
        # Validate that the receiving employee exists
        TD.get_emps(employee=to_emp_id)
        # Get all tasks assigned to employee
        add_info = TD.make_add_info(emp_id=emp_id, to_emp_id=to_emp_id, add_req=add_req)
        return [tuition_info.json() for tuition_info in add_info.values()]

    # Get all the additional info requested of you
    @classmethod
    def get_all_add_info(cls, emp_id=None):
        # Validate that the requesting employee exists
        TD.get_emps(employee=emp_id)
        # Get all tasks assigned to employee
        add_info = TD.find_all_add_info(to_emp_id=emp_id)
        return [tuition_info.json() for tuition_info in add_info.values()]

    # Update your application with the new final grade
    @classmethod
    def update_app_data(cls, emp_id=None, app_id=None, app_data=None):
        # Validate that the requesting employee exists
        TD.get_emps(employee=emp_id)
        # Update your final grade
        add_info = TD.update_app_data(emp_id=emp_id, app_id=app_id, app_data=app_data)
        return [tuition_info.json() for tuition_info in add_info.values()]

    # Find emp id by app role
    @classmethod
    def find_emp_by_approle(cls, app_id=None, emp_type=None):
        response_holder = {"emp_id": 0}
        # Validate that the app exists
        app_hold = TD.get_apps(app_data=app_id)
        print(app_hold[0])
        if emp_type == "sup_approval":
            # Find the work order data by work id
            hold_work = TD.find_work_order(work_id=app_hold[0].sup_approval)
            response_holder["emp_id"] = hold_work[0].emp_id
        elif emp_type == "dept_approval":
            # Find the work order data by work id
            hold_work = TD.find_work_order(work_id=app_hold[0].dept_approval)
            response_holder["emp_id"] = hold_work[0].emp_id
        elif emp_type == "emp":
            print(app_hold)
            response_holder["emp_id"] = app_hold[0].emp_id
        return response_holder

    # Search for all the work that belongs to this employee
    @classmethod
    def get_level(cls, employee=None):
        # Validate that the employee exists
        TD.get_emps(employee=employee)
        # Get all tasks assigned to employee
        valid_emps = TD.get_level(emp_id=employee)
        return valid_emps

    # Get the total reimbursed amount
    @classmethod
    def get_reamt(cls, emp_id=None):
        # Validate that the employee exists
        TD.get_emps(employee=emp_id)
        # Get the total amount that was reimbursed
        valid_emps = TD.get_re_amt(employee=emp_id)
        return valid_emps

    # Update a work order by ID
    @classmethod
    def update_work_by_id(cls, employee=None, work_id=None, work_data=None):
        # Validate that the employee exists
        TD.get_emps(employee=employee)
        # Validate that the work ID exists
        TD.find_work_order(work_id=work_id)
        # Update the Work Order
        valid_work = TD.update_work_order(work_id=work_id, work_data=work_data, employee=employee)
        if valid_work[0].approval:
            my_app = TD.get_apps(app_data=valid_work[0].app_id)
            if my_app[0].dept_approval is not None:
                if my_app[0].benco_approval is None or my_app[0].benco_approval == "null":
                    my_benco = TD.make_new_benco_approval(app_id=valid_work[0].app_id, emp_id=my_app[0].emp_id,
                                                          sup_id=employee)
                    TD.update_app_approval(app_id=valid_work[0].app_id, sup_approval_id=my_benco[0].work_id,
                                           approval_type="benco_approval")

            else:
                dept_head = TD.get_sup_by_emps(employee=employee)
                new_dept_approval = TD.make_new_dept_approval(app_id=valid_work[0].app_id, emp_id=dept_head[0].emp_id)
                TD.update_app_approval(app_id=valid_work[0].app_id, sup_approval_id=new_dept_approval[0].work_id,
                                       approval_type="dept_approval")
        return [tuition_info.json() for tuition_info in valid_work.values()]

    # Validate the application was completed properly
    @classmethod
    def validate_application(cls, sub_app=None):
        # check if application was not filled out
        if sub_app is None:
            raise AppNotCompleted(
                f"Your application was not completed please complete the required fields!", loc=f" | Level:{__name__}")
        # validate user input username
        else:
            # checks if address was completed
            if "address" not in dict(sub_app):
                raise AppNotCompleted(f"Please fill in your address!", loc=f" | Level:{__name__}")
            elif sub_app["address"] is None:
                raise AppNotCompleted(f"Please fill in your address!", loc=f" | Level:{__name__}")
            # checks if city was completed
            if "city" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide your city!", loc=f" | Level:{__name__}")
            elif sub_app["city"] is None:
                raise AppNotCompleted(f"Please provide your city!", loc=f" | Level:{__name__}")
            # checks if state was completed
            if "state" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide your state!", loc=f" | Level:{__name__}")
            elif sub_app["state"] is None:
                raise AppNotCompleted(f"Please provide your state!", loc=f" | Level:{__name__}")
            # checks if zip was completed
            if "zip" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide your zip!", loc=f" | Level:{__name__}")
            elif int(sub_app["zip"]) is None:
                raise AppNotCompleted(f"Please provide your zip!", loc=f" | Level:{__name__}")
            # checks if description was completed
            if "description" not in dict(sub_app):
                raise AppNotCompleted(f"Please give a description or the curriculum!", loc=f" | Level:{__name__}")
            elif sub_app["description"] is None:
                raise AppNotCompleted(f"Please give a description or the curriculum!", loc=f" | Level:{__name__}")
            # checks if work justification was completed
            if "work_just" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide a short description to justify the reason!",
                                      loc=f" | Level:{__name__}")
            elif sub_app["work_just"] is None:
                raise AppNotCompleted(f"Please provide a short description to justify the reason!",
                                      loc=f" | Level:{__name__}")
            # checks if the total price of the class was completed
            if "price_tag" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide the full cost!", loc=f" | Level:{__name__}")
            elif round(float(sub_app["price_tag"]), 2) is None:
                raise AppNotCompleted(f"Please provide the full cost!", loc=f" | Level:{__name__}")
            else:
                sub_app["price_tag"] = round(float(sub_app["price_tag"]), 2)
            # checks if the event type was completed
            if "event_types" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide what type of event it is!", loc=f" | Level:{__name__}")
            elif sub_app["event_types"] != "courses" and sub_app["event_types"] != "seminars" and sub_app[
                "event_types"] != "certification preparation classes" and sub_app["event_types"] != "certification" and \
                    sub_app["event_types"] != "technical training" and sub_app["event_types"] != "other":
                raise AppNotCompleted(f"Please provide a valid event type!", loc=f" | Level:{__name__}")
            else:
                if "refunded_amt" not in dict(sub_app) or sub_app["refunded_amt"] is None:
                    if sub_app["event_types"] == "courses":
                        sub_app["refunded_amt"] = round(float(sub_app["price_tag"] * 0.8), 2)
                    elif sub_app["event_types"] == "seminars":
                        sub_app["refunded_amt"] = round(float(sub_app["price_tag"] * 0.6), 2)
                    elif sub_app["event_types"] == "certification preparation classes":
                        sub_app["refunded_amt"] = round(float(sub_app["price_tag"] * 0.75), 2)
                    elif sub_app["event_types"] == "certification":
                        sub_app["refunded_amt"] = round(float(sub_app["price_tag"]), 2)
                    elif sub_app["event_types"] == "technical training":
                        sub_app["refunded_amt"] = round(float(sub_app["price_tag"] * 0.9), 2)
                    elif sub_app["event_types"] == "other":
                        sub_app["refunded_amt"] = round(float(sub_app["price_tag"] * 0.3), 2)
                else:
                    sub_app["refunded_amt"] = round(float(sub_app["refunded_amt"]), 2)
            # checks if the grade format was completed
            if "grade_format" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide the grading format!", loc=f" | Level:{__name__}")
            elif sub_app["grade_format"] != "grade" and sub_app[
                "grade_format"] != "presentation":
                raise AppNotCompleted(f"Please provide a valid grading format!", loc=f" | Level:{__name__}")
            # checks if supervisor approval was provided
            if "sup_approval" in dict(sub_app):
                if sub_app["sup_approval"] == "null":
                    sub_app.pop("sup_approval")
            # checks if dept head approval was completed
            if "dept_approval" in dict(sub_app):
                if sub_app["dept_approval"] == "null":
                    sub_app.pop("dept_approval")
            # checks if the date of the event was completed
            if "date_event" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide the date of the event!", loc=f" | Level:{__name__}")
            elif sub_app["date_event"] is None:
                raise AppNotCompleted(f"Please provide the date of the event!", loc=f" | Level:{__name__}")
            # Checks if you have missed hours filled in
            if "missed_time" not in dict(sub_app):
                raise AppNotCompleted(f"Please provide the total hours that will be missed!",
                                      loc=f" | Level:{__name__}")
            elif float(sub_app["missed_time"]) is None:
                raise AppNotCompleted(f"Please provide the total hours that will be missed!",
                                      loc=f" | Level:{__name__}")
        return "Application Complete!"

    @classmethod
    def validate_username(cls, username=None):
        # validate user input username
        if username is not None:
            username = username.lower()
            if len(username) < 8:
                raise InvalidValue("Your username needs to be at least 8 char!")
            elif len(username) > 15:
                raise InvalidValue("Your username cannot be more than 15 char!")
            elif re.findall("[^a-zA-Z0-9.]", username):
                raise InvalidValue("Your username may only use letters numbers or a period!")
            else:
                if not re.findall("[a-zA-Z]", username):
                    raise InvalidValue("Your username must have at least 1 letter!")
                if re.findall("^[0-9.]", username):
                    raise InvalidValue("Your username cannot start with a number or period!")
                if re.findall("[.]$", username):
                    raise InvalidValue("Your username cannot end with a period!")
            return username
        else:
            raise InvalidValue("No value Given!")

    @classmethod
    def validate_password(cls, password=None):
        # validate user input password
        if password is not None:
            if len(password) < 8:
                raise InvalidValue("Your password needs to be at least 8 char!")
            elif len(password) > 15:
                raise InvalidValue("Your password cannot be more than 15 char!")
            elif re.findall("[^a-zA-Z0-9!.@(_#)]", password):
                raise InvalidValue("Your password may only use letters numbers or these symbols: !.@(_#)")
            else:
                if not re.findall("[0-9]", password):
                    raise InvalidValue("Your password must have at least one number!")
                if not re.findall("[a-zA-Z]", password):
                    raise InvalidValue("Your password must have at least 1 letter!")
                if not re.findall("[A-Z]", password):
                    raise InvalidValue("Your password must have at least 1 uppercase letter!")
                if not re.findall("[a-z]", password):
                    raise InvalidValue("Your password must have at least 1 lowercase letter!")
                if not re.findall("[!.@(_#)]", password):
                    raise InvalidValue("Your password must have at least 1 special symbol: !.@(_#)")
            return password
        else:
            raise InvalidValue("No value Given!")


if __name__ == "__main__":
    print(__name__)
