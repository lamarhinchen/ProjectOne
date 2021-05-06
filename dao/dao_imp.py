import datetime
import random as rand
from cust_exceptions.access_denied import AccessDenied
from cust_exceptions.acct_already_exists import AcctAlreadyExists
from cust_exceptions.app_not_completed import AppNotCompleted
from cust_exceptions.invalid_value import InvalidValue
from cust_exceptions.no_work_exists import NoWorkExists
from db_model.db_conn import DbConn as Apps
from cust_exceptions.acct_does_not_exist import AcctDoesNotExist
from cust_logging.my_logger import MyLog as Log_Me


class TuitionDao:

    # File a new Application
    @classmethod
    def file_application(cls, new_app):
        data_names = ""
        data_values = ""
        for app_parts in new_app:
            if data_names != "":
                data_names += f", {app_parts}"
                data_values += ", %s"
            else:
                data_names += f"{app_parts}"
                data_values += "%s"
        Log_Me.info_log(f"data_names:{data_names} and data_values:{data_values} | Level:{__name__}")
        # Set up input values
        tuple_holder = tuple(new_app.values())
        # load result set from data base
        db_view = Apps.make_connect(
            f"""insert into application({data_names}) values({data_values}) RETURNING *;""",
            tuple_holder)
        # Puts the approval to correct supervisor
        cls.file_initial_approval(application_data=db_view)
        Log_Me.info_log(f"Application update:{db_view} | Level:{__name__}")
        return db_view

    # Get an employee, if id=None get all the employees
    @classmethod
    def get_emps(cls, employee=None):
        if employee is None:
            # Load result set from data base
            db_view = Apps.emp_make_connect("SELECT * FROM employees WHERE disabled=false;")
            if len(db_view) == 0:
                raise AcctDoesNotExist("There are no employees!", loc=f" | Level:{__name__}")
            # Return all employees
            return [tuition_info.json() for tuition_info in db_view.values()]
        else:
            # Return one employee
            # Load result set from data base
            tuple_holder = (int(employee),)
            db_view = Apps.emp_make_connect("""SELECT * FROM employees WHERE emp_id=%s AND disabled=false;""",
                                            tuple_holder)
            if len(db_view) == 0:
                raise AcctDoesNotExist(f"empID: {employee} does not exist!", loc=f" | Level:{__name__}")
            return [tuition_info.json() for tuition_info in db_view.values()]

    # Get an application, if id=None get all the employees
    @classmethod
    def get_apps(cls, app_data=None):
        if app_data is None:
            raise InvalidValue("You must submit a valid application ID", loc=f" | Level:{__name__}")
        else:
            # Return one application
            # Load result set from data base
            tuple_holder = (int(app_data),)
            db_view = Apps.make_connect("""SELECT * FROM application WHERE app_id=%s;""",
                                        tuple_holder)
            if len(db_view) == 0:
                raise AcctDoesNotExist(f"The application ID does not exist!", loc=f" | Level:{__name__}")
            return db_view

    # Get all the applications that an employee filed
    @classmethod
    def get_all_my_apps(cls, emp_id=None):
        if emp_id is None:
            raise InvalidValue("You must submit a valid Employee ID", loc=f" | Level:{__name__}")
        else:
            # Return one application
            # Load result set from data base
            tuple_holder = (int(emp_id),)
            db_view = Apps.make_connect("""SELECT * FROM application WHERE emp_id=%s;""",
                                        tuple_holder)
            if len(db_view) == 0:
                raise AcctDoesNotExist(f"You have not filed any applications!", loc=f" | Level:{__name__}")
            return db_view

    # Get all of the work an employee
    @classmethod
    def find_work(cls, employee=None):
        if employee is None:
            raise InvalidValue("Please submit a valid employee ID!", loc=f" | Level:{__name__}")
        else:
            # Return one employees workload
            # Load result set from data base
            tuple_holder = (int(employee),)
            db_view = Apps.work_list_connect("""SELECT * FROM work_list WHERE emp_id=%s ORDER BY urgency_level desc;""",
                                             tuple_holder)
            if len(db_view) == 0:
                raise NoWorkExists(f"You do not have any work to complete!", loc=f" | Level:{__name__}")
            return db_view

    # Get the work order by the work order ID
    @classmethod
    def find_work_order(cls, work_id=None):
        if work_id is None:
            raise InvalidValue("Please submit a valid Work ID!", loc=f" | Level:{__name__}")
        else:
            # Return one employees workload
            # Load result set from data base
            tuple_holder = (int(work_id),)
            db_view = Apps.work_list_connect("""SELECT * FROM work_list WHERE work_id=%s;""",
                                             tuple_holder)
            if len(db_view) == 0:
                raise NoWorkExists(f"This work order ID does not exist!", loc=f" | Level:{__name__}")
            return db_view

    # Get the level of the employee
    @classmethod
    def get_level(cls, emp_id=None):
        if int(emp_id) is None:
            raise InvalidValue("Please submit a valid employee ID!", loc=f" | Level:{__name__}")
        else:
            position = {"position": "regular"}
            # Are they a reg employee
            # Load result set from data base
            tuple_holder = (int(emp_id),)
            db_view = Apps.misc_connect("""SELECT * FROM employee_work WHERE emp_id=%s;""",
                                             tuple_holder)
            if len(db_view) == 0:
                # Are they a supervisor
                # Load result set from data base
                tuple_holder = (int(emp_id),)
                db_view = Apps.misc_connect("""SELECT * FROM work_group WHERE sup_id=%s;""",
                                            tuple_holder)
                if len(db_view) == 0:
                    # Are they a dept head
                    # Load result set from data base
                    tuple_holder = (int(emp_id),)
                    db_view = Apps.misc_connect("""SELECT * FROM dept WHERE depthead_id=%s;""",
                                                tuple_holder)
                    if len(db_view) <= 0:
                        raise AcctDoesNotExist(f"This employee has not been positioned in the company yet!", loc=f" | Level:{__name__}")
                    else:
                        position["position"] = "depthead"
                else:
                    position["position"] = "supervisor"
            else:
                position["position"] = db_view[0][2]
            return position

    # Update the approval data
    @classmethod
    def update_work_order(cls, work_id=None, work_data=None, employee=None):
        if work_id is None:
            raise InvalidValue("Please submit a valid Work ID!", loc=f" | Level:{__name__}")
        else:
            if work_data["approval"] is not None or work_data["approval"] != "null":
                work_data["date_completed"] = datetime.datetime.now()
            # Load result set from data base
            tuple_holder = (
                work_data["urgency_level"], work_data["description"], work_data["approval"],
                work_data["date_completed"],
                int(work_id), employee)
            db_view = Apps.work_list_connect(
                f"""UPDATE work_list SET urgency_level=%s, description=%s, approval=%s, date_completed=%s WHERE work_id=%s AND emp_id=%s RETURNING *;""",
                tuple_holder)
            if len(db_view) == 0:
                raise NoWorkExists(f"The work order does not exist!", loc=f" | Level:{__name__}")
            return db_view

    # Update the additional info request
    @classmethod
    def update_add_info(cls, info_id=None, up_req=None):
        if info_id is None or up_req is None:
            raise InvalidValue("Please submit the additional information requested!", loc=f" | Level:{__name__}")
        else:
            if "date_completed" in dict(up_req):
                if up_req["date_completed"] is None or up_req["date_completed"] == "null":
                    up_req["date_completed"] = datetime.datetime.now()
            else:
                up_req["date_completed"] = datetime.datetime.now()
            # Load result set from data base
            tuple_holder = (
                 up_req["reason"], up_req["date_completed"], int(info_id))
            db_view = Apps.work_list_connect(
                f"""UPDATE add_info SET reason=%s, date_completed=%s WHERE info_id=%s RETURNING *;""",
                tuple_holder)
            if len(db_view) == 0:
                raise NoWorkExists(f"The work order was not successfully updated!", loc=f" | Level:{__name__}")
            return db_view

    # Get employee by email
    @classmethod
    def get_emps_by_email(cls, employee=None):
        if employee is None:
            raise InvalidValue("To login please give your email!", loc=f" | Level:{__name__}")
        else:
            # Return one employee
            # Load result set from data base
            tuple_holder = (employee["email"],)
            db_view = Apps.emp_make_connect("""SELECT * FROM employees WHERE email=%s AND disabled=false;""",
                                            tuple_holder)
            if len(db_view) == 0:
                raise AcctDoesNotExist(f"Employee email: {employee} does not exist!", loc=f" | Level:{__name__}")
            return db_view

    # Search for a list of employees via email
    @classmethod
    def search_emps_by_email(cls, employee=None):
        if employee is None:
            raise InvalidValue("No employees found!", loc=f" | Level:{__name__}")
        else:
            # Return one employee
            # Load result set from data base
            tuple_holder = (str(employee) + "%",)
            db_view = Apps.emp_make_connect(
                """SELECT * FROM employees WHERE email LIKE %s AND disabled=false ORDER BY email Asc LIMIT 5;""",
                tuple_holder)
            if len(db_view) == 0:
                raise AcctDoesNotExist(f"No employees with this email exist!", loc=f" | Level:{__name__}")
            return db_view

    # Create the additional information request
    @classmethod
    def make_add_info(cls, emp_id=None, to_emp_id=None, add_req=None):
        if emp_id is None or to_emp_id is None:
            raise InvalidValue("No employees found!", loc=f" | Level:{__name__}")
        else:
            add_req["from_emp_id"] = emp_id
            add_req["to_emp_id"] = to_emp_id
            db_view = cls.find_add_info(emp_id=emp_id, to_emp_id=to_emp_id, add_req=add_req)
            if len(db_view) > 0:
                raise AcctAlreadyExists("This request was already made, no need to make another!", loc=f" | Level:{__name__}")
            data_names = ""
            data_values = ""
            for app_parts in add_req:
                if data_names != "":
                    data_names += f", {app_parts}"
                    data_values += ", %s"
                else:
                    data_names += f"{app_parts}"
                    data_values += "%s"
            # Makes one additional info request
            # Load result set from data base
            tuple_holder = [tuition_info for tuition_info in add_req.values()]
            db_view = Apps.add_info_connect(
                f"""INSERT INTO add_info({data_names}) values({data_values}) RETURNING *;""",
                tuple_holder)
            return db_view

    # Find add info
    @classmethod
    def find_add_info(cls, emp_id=None, to_emp_id=None, add_req=None):
        if emp_id is None or to_emp_id is None:
            raise InvalidValue("No employees found!", loc=f" | Level:{__name__}")
        else:
            add_req["from_emp_id"] = emp_id
            add_req["to_emp_id"] = to_emp_id
            del add_req['reason']
            data_names = ""
            for app_parts in add_req:
                if data_names != "":
                    data_names += f"AND {app_parts}=%s"
                else:
                    data_names += f"{app_parts}=%s"
            # Finds the single instance of this additional request
            # Load result set from data base
            tuple_holder = [tuition_info for tuition_info in add_req.values()]
            db_view = Apps.add_info_connect(
                f"""SELECT * FROM add_info WHERE {data_names};""",
                tuple_holder)
            return db_view

    # Find add info
    @classmethod
    def find_add_info_by_info_id(cls, emp_id=None, info_id=None):
        if emp_id is None or info_id is None:
            raise InvalidValue("No employees found!", loc=f" | Level:{__name__}")
        else:
            add_req = {"to_emp_id": emp_id, "info_id": info_id}
            data_names = ""
            for app_parts in add_req:
                if data_names != "":
                    data_names += f"AND {app_parts}=%s"
                else:
                    data_names += f"{app_parts}=%s"
            # Finds the single instance of this additional request
            # Load result set from data base
            tuple_holder = [tuition_info for tuition_info in add_req.values()]
            db_view = Apps.add_info_connect(
                f"""SELECT * FROM add_info WHERE {data_names};""",
                tuple_holder)
            if len(db_view) <= 0:
                raise NoWorkExists("This additional request does not exist!", loc=f" | Level:{__name__}")
            return db_view

    # Find all the info requests made to you
    @classmethod
    def find_all_add_info(cls, to_emp_id=None):
        if to_emp_id is None:
            raise InvalidValue("Incorrect value for employee id!", loc=f" | Level:{__name__}")
        else:
            add_req = {"to_emp_id": to_emp_id}
            print("Find values")
            print(add_req.values())
            data_names = ""
            for app_parts in add_req:
                if data_names != "":
                    data_names += f"AND {app_parts}=%s"
                else:
                    data_names += f"{app_parts}=%s"
            # Finds all the info requests for an employee
            # Load result set from data base
            tuple_holder = [tuition_info for tuition_info in add_req.values()]
            db_view = Apps.add_info_connect(
                f"""SELECT * FROM add_info WHERE {data_names};""",
                tuple_holder)
            return db_view

    # Get the supervisor of the employee by their ID
    @classmethod
    def get_sup_by_emps(cls, employee=None):
        print(employee)
        if employee is None:
            raise InvalidValue("No employee information provided!", loc=f" | Level:{__name__}")
        else:
            # Return the employees supervisor
            # Load result set from data base
            # Find the group the employee is attached to
            tuple_holder = (int(employee),)
            db_view = Apps.misc_connect("""SELECT group_id FROM employee_work WHERE emp_id=%s;""",
                                        tuple_holder)
            # If they are not a reg employee
            if len(db_view) == 0:
                # Find the dept you are in
                tuple_holder = (int(employee),)
                db_view = Apps.misc_connect("""SELECT dept_id FROM work_group WHERE sup_id=%s;""",
                                            tuple_holder)
                # If they are not a supervisor then they are a dept head and no one is higher
                if len(db_view) == 0:
                    # Find the dept head
                    tuple_holder = (int(employee),)
                    db_view = Apps.misc_connect("""SELECT depthead_id FROM dept WHERE depthead_id=%s;""",
                                                tuple_holder)
                else:
                    # Find the dept head if they are a supervisor and no sup is above them
                    tuple_holder = (int(db_view[0][0]),)
                    db_view = Apps.misc_connect("""SELECT depthead_id FROM dept WHERE dept_id=%s;""",
                                                tuple_holder)
            else:
                # Find the supervisor of that group
                tuple_holder = (int(db_view[0][0]),)
                db_view = Apps.misc_connect("""SELECT sup_id FROM work_group WHERE group_id=%s;""",
                                            tuple_holder)
            # Find the supervisor's info
            if db_view is None:
                raise InvalidValue("You are not yet assigned to any work-group! Please notify mgmt to assign you.", loc=f" | Level:{__name__}")
            tuple_holder = (int(db_view[0][0]),)
            db_view = Apps.emp_make_connect("""SELECT * FROM employees WHERE emp_id=%s AND disabled=false;""",
                                            tuple_holder)
            if len(db_view) == 0:
                raise AcctDoesNotExist(f"empID: {employee} does not exist!", loc=f" | Level:{__name__}")
            return db_view

    # Get an employee, if id=None get all the employees
    @classmethod
    def file_initial_approval(cls, application_data=None):
        if application_data is None:
            # Raise error there needs to be application data
            raise AppNotCompleted("You must first file an application to get approvals!", loc=f" | Level:{__name__}")
        else:
            # Find out who the supervisor is
            app_holder = application_data[0]
            my_sup = cls.get_sup_by_emps(employee=app_holder.emp_id)
            # Holds the data required to file for an approval
            approval_matrix = {"emp_id": my_sup[0].emp_id, "app_id": app_holder.app_id}
            Log_Me.info_log(f"sup id:{my_sup[0].emp_id} and your id:{app_holder.emp_id} | Level:{__name__}")
            if app_holder.sup_approval_attach is True or app_holder.emp_id == my_sup[0].emp_id:
                approval_matrix["date_completed"] = datetime.datetime.now()
                approval_matrix["approval"] = True
            if datetime.datetime.now() + datetime.timedelta(days=11) > app_holder.date_event:
                approval_matrix["urgency_level"] = 75
            elif datetime.datetime.now() + datetime.timedelta(weeks=2) > app_holder.date_event:
                approval_matrix["urgency_level"] = 50
            data_names = ""
            data_values = ""
            for app_parts in approval_matrix:
                if data_names != "":
                    data_names += f", {app_parts}"
                    data_values += ", %s"
                else:
                    data_names += f"{app_parts}"
                    data_values += "%s"
            Log_Me.info_log(f"data_names:{data_names} and data_values:{data_values} | Level:{__name__}")
            # Set up input values
            tuple_holder = tuple(approval_matrix.values())
            # Return the approval needed to file
            # Load result set from data base
            db_view = Apps.work_list_connect(
                F"""INSERT INTO work_list({data_names}) values({data_values}) RETURNING *;""",
                tuple_holder)
            db_holder = db_view[0]
            cls.update_app_approval(app_id=db_holder.app_id, sup_approval_id=db_holder.work_id,
                                    approval_type="sup_approval")
            # Check if the supervisor is the department head
            dept_head = cls.get_sup_by_emps(employee=my_sup[0].emp_id)
            if my_sup[0].emp_id == dept_head[0].emp_id:
                cls.update_app_approval(app_id=db_holder.app_id, sup_approval_id=db_holder.work_id,
                                        approval_type="dept_approval")
                if "approval" in dict(approval_matrix):
                    if approval_matrix["approval"] is True:
                        benco_app = cls.make_new_benco_approval(app_id=app_holder.app_id, emp_id=app_holder.emp_id,
                                                                sup_id=my_sup[0].emp_id)
                        cls.update_app_approval(app_id=db_holder.app_id, sup_approval_id=benco_app[0].work_id,
                                                approval_type="benco_approval")
            elif app_holder.sup_approval_attach is True:
                # Make new dept approval but don't auto approve
                new_dept_approval = cls.make_new_dept_approval(app_id=db_holder.app_id, emp_id=dept_head[0].emp_id)
                cls.update_app_approval(app_id=db_holder.app_id, sup_approval_id=new_dept_approval[0].work_id,
                                        approval_type="dept_approval")
            Log_Me.info_log(f"supervisor worklist:{db_view} | Level:{__name__}")
            return db_view

    # Make a new benco approval if the other two approvals are complete
    @classmethod
    def make_new_benco_approval(cls, app_id=None, emp_id=None, sup_id=None):
        # Find a benco that is not you or your supervisor
        tuple_holder = (int(emp_id), int(sup_id))
        db_view = Apps.misc_connect(
            """SELECT emp_id FROM employee_work WHERE group_id=3 AND emp_id!=%s AND emp_id!=%s;""",
            tuple_holder)
        rand_benco = db_view[rand.randint(0, len(db_view) - 1)][0]
        # Holds the data required to file for an approval
        approval_matrix = {"emp_id": rand_benco, "app_id": app_id}
        app_holder = cls.get_apps(app_data=app_id)
        app_holder = app_holder[0]
        if datetime.datetime.now() + datetime.timedelta(days=11) > app_holder.date_event:
            approval_matrix["urgency_level"] = 75
        elif datetime.datetime.now() + datetime.timedelta(weeks=2) > app_holder.date_event:
            approval_matrix["urgency_level"] = 50
        data_names = ""
        data_values = ""
        for app_parts in approval_matrix:
            if data_names != "":
                data_names += f", {app_parts}"
                data_values += ", %s"
            else:
                data_names += f"{app_parts}"
                data_values += "%s"
        Log_Me.info_log(f"Benco:{data_names} and Benco vals:{data_values} | Level:{__name__}")
        # Set up input values
        tuple_holder = tuple(approval_matrix.values())
        # Return the benco worklist
        # Load result set from data base
        db_view = Apps.work_list_connect(
            F"""INSERT INTO work_list({data_names}) values({data_values}) RETURNING *;""",
            tuple_holder)
        return db_view

    # Make a new dept head approval
    @classmethod
    def make_new_dept_approval(cls, app_id=None, emp_id=None):
        # Holds the data required to file for an approval
        app_holder = cls.get_apps(app_data=app_id)
        app_holder = app_holder[0]
        approval_matrix = {"emp_id": emp_id, "app_id": app_id}
        # Sets the urgency level based on the date
        print(datetime.datetime.now() + datetime.timedelta(days=11) > app_holder.date_event)
        if datetime.datetime.now() + datetime.timedelta(days=11) > app_holder.date_event:
            approval_matrix["urgency_level"] = 75
            print(approval_matrix["urgency_level"])
        elif datetime.datetime.now() + datetime.timedelta(weeks=2) > app_holder.date_event:
            approval_matrix["urgency_level"] = 50
            print(approval_matrix["urgency_level"])
        data_names = ""
        data_values = ""
        for app_parts in approval_matrix:
            if data_names != "":
                data_names += f", {app_parts}"
                data_values += ", %s"
            else:
                data_names += f"{app_parts}"
                data_values += "%s"
        Log_Me.info_log(f"Dept Head:{data_names} and Dept vals:{data_values} | Level:{__name__}")
        # Set up input values
        tuple_holder = tuple(approval_matrix.values())
        # Return the dept head worklist
        # Load result set from data base
        db_view = Apps.work_list_connect(
            F"""INSERT INTO work_list({data_names}) values({data_values}) RETURNING *;""",
            tuple_holder)
        return db_view

    # Update application with approval ID
    @classmethod
    def update_app_approval(cls, app_id=None, sup_approval_id=None, approval_type=None):
        # Set up input values
        tuple_holder = (sup_approval_id, app_id)
        # Return the approval needed to file
        # Load result set from data base
        if approval_type == "sup_approval":
            db_view = Apps.make_connect(F"""UPDATE application SET sup_approval=%s WHERE app_id=%s RETURNING *;""",
                                        tuple_holder)
            return db_view
        elif approval_type == "dept_approval":
            db_view = Apps.make_connect(F"""UPDATE application SET dept_approval=%s WHERE app_id=%s RETURNING *;""",
                                        tuple_holder)
            return db_view
        elif approval_type == "benco_approval":
            db_view = Apps.make_connect(F"""UPDATE application SET benco_approval=%s WHERE app_id=%s RETURNING *;""",
                                        tuple_holder)
            return db_view

    # Get total amount reimbursed
    @classmethod
    def get_re_amt(cls, employee=None):
        # Find out the total amount that could be reimbursed
        tuple_holder = (int(employee),)
        db_view = Apps.misc_connect(
            """select emp_id, count(app_id) as total_apps, sum(refunded_amt) as total_refund from application where emp_id = %s and extract(year from date_event) = extract(year from NOW()) group by emp_id;""",
            tuple_holder)
        total_amt = db_view
        if len(total_amt) <= 0:
            raise AcctDoesNotExist("No valid applications found!", loc=f" | Level:{__name__}")
        Log_Me.info_log(f"Getting total reimbursed amount:{total_amt} | Level:{__name__}")

        # Get all the apps you submitted
        tuple_holder = (int(employee),)
        db_view = Apps.misc_connect(
            """select app_id from application where emp_id = %s and extract(year from date_event) = extract(year from NOW());""",
            tuple_holder)
        Log_Me.info_log(f"Getting all the applications you submitted:{db_view} | Level:{__name__}")
        all_my_apps = db_view
        if len(all_my_apps) <= 0:
            raise AcctDoesNotExist("No valid applications found!", loc=f" | Level:{__name__}")
        # Get all the denied apps
        approval_matrix = {}
        data_names = ""
        counter = 0
        for app_parts in all_my_apps:
            if data_names != "":
                data_names += f"or app_id=%s"
            else:
                data_names += f"app_id=%s"
            approval_matrix[f"me_val{counter}"] = app_parts[0]
            counter += 1
        tuple_holder = [temp_val for temp_val in approval_matrix.values()]
        db_view = Apps.misc_connect(
            f"""select app_id as denied from work_list where approval=false and ({data_names}) group by app_id;""",
            tuple_holder)
        Log_Me.info_log(f"Getting the apps that were denied:{db_view} | Level:{__name__}")
        reimburse_val = {"emp_id": int(employee), "total_apps": total_amt[0][1], "total_apps_denied": 0, "total_refund_denied": 0, "total_refund": round(float(total_amt[0][2]), 2), "calculated_refund": 0}
        if len(db_view) > 0:
            total_apps_denied = db_view
            # Total amount that was denied
            approval_matrix = {"emp_id": int(employee)}
            data_names = ""
            counter = 0
            for app_parts in total_apps_denied:
                if data_names != "":
                    data_names += f"or app_id=%s"
                else:
                    data_names += f"app_id=%s"
                approval_matrix[f"me_val{counter}"] = app_parts[0]
                counter += 1
            reimburse_val["total_apps_denied"] = counter
            tuple_holder = [temp_val for temp_val in approval_matrix.values()]
            print(tuple_holder)
            db_view = Apps.misc_connect(
                f"""select emp_id, count(app_id) as total_apps, sum(refunded_amt) as total_refund from application where emp_id = %s and {data_names} and extract(year from date_event) = extract(year from NOW()) group by emp_id;""",
                tuple_holder)
            denied_amt = db_view
            Log_Me.info_log(f"Getting total denied amount:{denied_amt} | Level:{__name__}")
            if len(denied_amt) > 0:
                reimburse_val["total_refund_denied"] = round(float(denied_amt[0][2]), 2)
        if reimburse_val["total_refund"] - reimburse_val["total_refund_denied"] >= 1000:
            reimburse_val["calculated_refund"] = 1000
        else:
            reimburse_val["calculated_refund"] = reimburse_val["total_refund"] - reimburse_val["total_refund_denied"]
        return reimburse_val


if __name__ == "__main__":
    print(TuitionDao.get_emps())
