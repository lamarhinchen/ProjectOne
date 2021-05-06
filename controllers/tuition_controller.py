from psycopg2 import Error
from cust_exceptions.app_not_completed import AppNotCompleted
from cust_exceptions.access_denied import AccessDenied
from cust_exceptions.acct_already_exists import AcctAlreadyExists
from cust_exceptions.acct_does_not_exist import AcctDoesNotExist
from cust_exceptions.incorrect_money_value import IncorrectMoneyValue
from cust_exceptions.invalid_value import InvalidValue
from cust_exceptions.no_funds_available import NoFundsAvailable
from cust_exceptions.no_work_exists import NoWorkExists
from cust_logging.my_logger import MyLog as Log_Me
from flask import jsonify, request
from services.tuition_service import TuitionService as services

# welcome message in the logger
Log_Me.info_log(
    f"Tuition Reimbursement Program Started! | Level:{__name__}")  # Would replace using print("Program Started")


def route(app):
    # Welcome message
    @app.route('/', methods=["GET", "POST"])
    def hello_world():
        Log_Me.info_log(f"The home page was loaded! | Level:{__name__}")
        return "Welcome to the Tuition Reimbursement Program!", 200

    # Page not found message
    @app.errorhandler(404)
    def page_not_found(e):
        # how to load a custom page not found template doc
        # return render_template('404.html'), 404
        Log_Me.info_log(f"{e} | Level:{__name__}")
        return "Page Not Found!", 404

    # Find an employee by their ID
    @app.route("/users/<emp_id>", methods=["GET"])
    def get_employee_by_id(emp_id):
        try:
            # Validating Employee ID
            employee = int(emp_id)
            # Serializing data to find employee
            application_info = jsonify(services.get_employee_by_id(employee=employee))
            Log_Me.info_log(f"employeeID: {employee} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Find an employee worklist by their ID
    @app.route("/users/<emp_id>/work", methods=["GET"])
    def get_employee_work(emp_id):
        try:
            # Validating Employee ID
            employee = int(emp_id)
            # Serializing data to find employee tasks
            work_info = jsonify(services.get_employee_work(employee=emp_id))
            Log_Me.info_log(f"employeeID: {employee} | Level:{__name__}")
            return work_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except NoWorkExists as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Find all the applications an employee filed
    @app.route("/users/<emp_id>/apps", methods=["GET"])
    def get_all_my_apps(emp_id):
        try:
            # Serializing data to find employee tasks
            work_info = jsonify(services.get_all_my_apps(emp_id=int(emp_id)))
            Log_Me.info_log(f"employeeID: {emp_id} | Level:{__name__}")
            return work_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Find all the application data
    @app.route("/app/<app_id>", methods=["GET"])
    def get_application(app_id):
        try:
            # Validating app id
            employee = int(app_id)
            # Serializing data to find the application
            app_info = jsonify(services.get_app(app_data=app_id))
            Log_Me.info_log(f"employeeID: {employee} | Level:{__name__}")
            return app_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Find an employees supervisor
    @app.route("/users/<emp_id>/supervisor", methods=["GET"])
    def get_sup_by_employee_id(emp_id):
        try:
            # Validating Employee ID
            employee = int(emp_id)
            # Serializing data to find employee
            application_info = jsonify(services.get_sup_by_employee_id(employee=employee))
            Log_Me.info_log(f"employeeID: {employee} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Login so you can look at your work to complete
    @app.route("/login", methods=["POST"])
    def login_employee():
        try:
            # Serializing data to log in employee
            login_conf = jsonify(services.employee_login(request.json))
            Log_Me.info_log(f"""Welcome you are now logged in! | Level:{__name__}""")
            return login_conf, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Return all employees
    @app.route("/users", methods=["GET"])
    def get_all_employees():
        try:
            # Serializing data to return all employees
            application_info = jsonify(services.get_all_employees())
            Log_Me.info_log(f"employees: {application_info} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Return all employees related to search criteria
    @app.route("/search/<search_data>", methods=["GET"])
    def get_all_employees_search(search_data):
        try:
            # Serializing data to return all employees that meet search criteria
            search_info = jsonify(services.get_all_employees_search(search_data=search_data))
            Log_Me.info_log(f"employees: {search_info} | Level:{__name__}")
            return search_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Submit a new application
    @app.route("/users/<emp_id>/apply", methods=["POST"])
    def submit_application(emp_id):
        try:
            # Validating Employee ID
            employee = int(emp_id)
            # Serializing Json data to submit application
            application_info = jsonify(services.submit_app(employee=employee, sub_app=request.json))
            Log_Me.info_log(f"Your application was received! | Level:{__name__}")
            Log_Me.info_log(f"employeeID: {employee} | Level:{__name__}")
            Log_Me.info_log(f"json: {request.json} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AppNotCompleted as e:
            Log_Me.warning_log(f"Warning! Application not completed! {e}, code 400{e.loc}")
            return e.message, 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except NoFundsAvailable as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Get an employees level in the company
    @app.route("/users/<emp_id>/level", methods=["GET"])
    def get_level(emp_id):
        try:
            # Validating Employee ID
            employee = int(emp_id)
            # Serializing Json data to get the employee level
            application_info = jsonify(services.get_level(employee=emp_id))
            Log_Me.info_log(f"you got your level: {application_info} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Get the total reimbursed amount
    @app.route("/users/<emp_id>/revalue", methods=["GET"])
    def get_reimburse_amt(emp_id):
        try:
            # Validating Employee ID
            employee = int(emp_id)
            # Serializing Json data to submit application
            application_info = jsonify(services.get_reamt(emp_id=emp_id))
            Log_Me.info_log(f"employeeID: {employee} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Get the emp ids of the emp, sup or dept
    @app.route("/apps/<app_id>/roles/<emp_type>", methods=["GET"])
    def find_emp_by_approle(app_id, emp_type):
        try:
            # Serializing Json data to submit application
            application_info = jsonify(services.find_emp_by_approle(app_id=int(app_id), emp_type=emp_type))
            Log_Me.info_log(f"employeeID: {app_id} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Make an additional info request
    @app.route("/users/<emp_id>/addinfo/<to_emp_id>", methods=["post"])
    def make_add_info(emp_id, to_emp_id):
        try:
            # Serializing Json data to submit application
            application_info = jsonify(
                services.make_add_info(emp_id=int(emp_id), to_emp_id=int(to_emp_id), add_req=request.json))
            Log_Me.info_log(f"employeeID: {emp_id} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except AcctAlreadyExists as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Get all of the additional info requested of you
    @app.route("/users/<emp_id>/addinfo", methods=["GET"])
    def get_all_add_info(emp_id):
        try:
            # Serializing Json data to submit application
            application_info = jsonify(
                services.get_all_add_info(emp_id=int(emp_id)))
            Log_Me.info_log(f"employeeID: {emp_id} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except AcctAlreadyExists as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Update an additional info request
    @app.route("/users/<emp_id>/addinfo/<info_id>", methods=["PUT"])
    def update_add_info(emp_id, info_id):
        try:
            # Serializing Json data to submit application
            application_info = jsonify(
                services.update_add_info(emp_id=int(emp_id), info_id=int(info_id), up_req=request.json))
            Log_Me.info_log(f"employeeID: {emp_id} | Level:{__name__}")
            return application_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except AcctDoesNotExist as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except AcctAlreadyExists as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except NoWorkExists as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400

    # Update an approval
    @app.route("/users/<emp_id>/work/<work_id>", methods=["PATCH"])
    def update_approval(emp_id, work_id):
        try:
            # Validating Employee ID
            employee = int(emp_id)
            # Validating the approval id
            my_work = int(work_id)
            # Serializing data to find employee tasks
            work_info = jsonify(services.update_work_by_id(employee=employee, work_id=my_work, work_data=request.json))
            Log_Me.info_log(f"employeeID: {employee} | Level:{__name__}")
            return work_info, 200
        except Error as e:
            Log_Me.error_log(f"Error! {e}, code 400 | Level:{__name__}")
            return e, 400
        except ValueError:
            Log_Me.error_log(f"Error! Not a valid number, code 400")
            return "Not a valid number", 400
        except InvalidValue as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
        except NoWorkExists as e:
            Log_Me.error_log(f"Error! {e}, code 400{e.loc}")
            return e.message, 400
