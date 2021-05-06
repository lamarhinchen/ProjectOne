import psycopg2
from psycopg2 import Error
from data_model.app_model import AppModel as AP
from data_model.emp_model import EmpModel as EP
from data_model.work_list_model import WorkListModel as WL
from cust_logging.my_logger import MyLog as Log_Me
from db_model.conn_access_point import DatabaseConn as conn_cred
from data_model.additional_model import AddModel as Add


class DbConn:

    @staticmethod
    def make_connect(query=None, var_tuple=None):
        # holds the application data
        tuition_app = {}
        tuition_app.clear()
        connection = "No connection made yet!"
        cursor = connection
        try:
            # read connection parameters
            params = conn_cred.load_conn()
            # Connect to an existing database
            connection = psycopg2.connect(**params)
            # If you don't specify a query into this function then default to this
            if query is None:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Print PostgreSQL details
                Log_Me.info_log("PostgreSQL server information")
                Log_Me.info_log(connection.get_dsn_parameters())
                # Executing a SQL query
                cursor.execute("SELECT version();")
                # Fetch result
                record = cursor.fetchone()
                Log_Me.info_log("You are connected to - ")
                Log_Me.info_log(record)
            else:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Executing a SQL query
                cursor.execute(query, var_tuple)
                # Commit the SQL query
                connection.commit()
                # Fetch result
                record = cursor.fetchall()
                counter = 0
                for row in record:
                    tuition_app[counter] = AP(app_id=row[0], emp_id=row[1], address=row[2],
                                              address_second=row[3], city=row[4], state=row[5], zipcode=row[6],
                                              description=row[7], work_just=row[8], price_tag=row[9],
                                              refunded_amt=row[10], event_types=row[11], grade_format=row[12],
                                              sup_approval_attach=row[13],
                                              sup_approval=row[14], dept_approval=row[15], benco_approval=row[16],
                                              date_received=row[17], date_event=row[18], missed_time=row[19],
                                              min_grade=row[20])
                    counter += 1
                Log_Me.info_log("You are connected to Postgre here are your results - ")
                Log_Me.info_log(record)
                Log_Me.info_log(tuition_app)
                return tuition_app

        except (Exception, Error) as error:
            Log_Me.error_log("Error while connecting to PostgreSQL")
            Log_Me.error_log(error)
            raise error
        finally:
            if connection:
                cursor.close()
                connection.close()
                Log_Me.info_log("PostgreSQL connection is closed")

    # Create the Employee database model
    @staticmethod
    def emp_make_connect(query=None, var_tuple=None):
        # holds the application data
        tuition_app = {}
        tuition_app.clear()
        connection = "No connection made yet!"
        cursor = connection
        try:
            # read connection parameters
            params = conn_cred.load_conn()
            # Connect to an existing database
            connection = psycopg2.connect(**params)
            # If you don't specify a query into this function then default to this
            if query is None:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Print PostgreSQL details
                Log_Me.info_log("PostgreSQL server information")
                Log_Me.info_log(connection.get_dsn_parameters())
                # Executing a SQL query
                cursor.execute("SELECT version();")
                # Fetch result
                record = cursor.fetchone()
                Log_Me.info_log("You are connected to - ")
                Log_Me.info_log(record)
            else:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Executing a SQL query
                cursor.execute(query, var_tuple)
                # Commit the SQL query
                connection.commit()
                # Fetch result
                record = cursor.fetchall()
                counter = 0
                for row in record:
                    tuition_app[counter] = EP(emp_id=row[0], firstname=row[1], middlename=row[2],
                                              lastname=row[3], email=row[4], disabled=row[5],
                                              date_employed=row[6], date_terminated=row[7])
                    counter += 1
                Log_Me.info_log("You are connected to Postgre here are your results - ")
                Log_Me.info_log(record)
                Log_Me.info_log(tuition_app)
                return tuition_app

        except (Exception, Error) as error:
            Log_Me.error_log("Error while connecting to PostgreSQL")
            Log_Me.error_log(error)
            raise error
        finally:
            if connection:
                cursor.close()
                connection.close()
                Log_Me.info_log("PostgreSQL connection is closed")

    # Create the Employee database model
    @staticmethod
    def work_list_connect(query=None, var_tuple=None):
        # holds the application data
        tuition_app = {}
        tuition_app.clear()
        connection = "No connection made yet!"
        cursor = connection
        try:
            # read connection parameters
            params = conn_cred.load_conn()
            # Connect to an existing database
            connection = psycopg2.connect(**params)
            # If you don't specify a query into this function then default to this
            if query is None:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Print PostgreSQL details
                Log_Me.info_log("PostgreSQL server information")
                Log_Me.info_log(connection.get_dsn_parameters())
                # Executing a SQL query
                cursor.execute("SELECT version();")
                # Fetch result
                record = cursor.fetchone()
                Log_Me.info_log("You are connected to - ")
                Log_Me.info_log(record)
            else:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Executing a SQL query
                cursor.execute(query, var_tuple)
                # Commit the SQL query
                connection.commit()
                # Fetch result
                record = cursor.fetchall()
                counter = 0
                for row in record:
                    tuition_app[counter] = WL(work_id=row[0], emp_id=row[1], app_id=row[2],
                                              urgency_level=row[3], description=row[4], approval=row[5],
                                              date_received=row[6], date_completed=row[7])
                    counter += 1
                Log_Me.info_log("You are connected to Postgre here are your results - ")
                Log_Me.info_log(record)
                Log_Me.info_log(tuition_app)
                return tuition_app

        except (Exception, Error) as error:
            Log_Me.error_log("Error while connecting to PostgreSQL")
            Log_Me.error_log(error)
            raise error
        finally:
            if connection:
                cursor.close()
                connection.close()
                Log_Me.info_log("PostgreSQL connection is closed")

    @staticmethod
    def add_info_connect(query=None, var_tuple=None):
        # holds the application data
        tuition_app = {}
        tuition_app.clear()
        connection = "No connection made yet!"
        cursor = connection
        try:
            # read connection parameters
            params = conn_cred.load_conn()
            # Connect to an existing database
            connection = psycopg2.connect(**params)
            # If you don't specify a query into this function then default to this
            if query is None:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Print PostgreSQL details
                Log_Me.info_log("PostgreSQL server information")
                Log_Me.info_log(connection.get_dsn_parameters())
                # Executing a SQL query
                cursor.execute("SELECT version();")
                # Fetch result
                record = cursor.fetchone()
                Log_Me.info_log("You are connected to - ")
                Log_Me.info_log(record)
            else:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Executing a SQL query
                cursor.execute(query, var_tuple)
                # Commit the SQL query
                connection.commit()
                # Fetch result
                record = cursor.fetchall()
                counter = 0
                for row in record:
                    tuition_app[counter] = Add(info_id=row[0], from_emp_id=row[1], to_emp_id=row[2],
                                               app_id=row[3], urgency_level=row[4], reason=row[5], date_received=row[6],
                                               date_completed=row[7])
                    counter += 1
                Log_Me.info_log("You are connected to Postgre here are your results - ")
                Log_Me.info_log(record)
                Log_Me.info_log(tuition_app)
                return tuition_app

        except (Exception, Error) as error:
            Log_Me.error_log("Error while connecting to PostgreSQL")
            Log_Me.error_log(error)
            raise error
        finally:
            if connection:
                cursor.close()
                connection.close()
                Log_Me.info_log("PostgreSQL connection is closed")

    # Create the Employee database model
    @staticmethod
    def misc_connect(query=None, var_tuple=None):
        connection = "No connection made yet!"
        cursor = connection
        try:
            # read connection parameters
            params = conn_cred.load_conn()
            # Connect to an existing database
            connection = psycopg2.connect(**params)
            # If you don't specify a query into this function then default to this
            if query is None:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Print PostgreSQL details
                Log_Me.info_log("PostgreSQL server information")
                Log_Me.info_log(connection.get_dsn_parameters())
                # Executing a SQL query
                cursor.execute("SELECT version();")
                # Fetch result
                record = cursor.fetchone()
                Log_Me.info_log("You are connected to - ")
                Log_Me.info_log(record)
            else:
                # Create a cursor to perform database operations
                cursor = connection.cursor()
                # Executing a SQL query
                cursor.execute(query, var_tuple)
                # Commit the SQL query
                connection.commit()
                # Fetch result
                record = cursor.fetchall()
                Log_Me.info_log("You are connected to Postgre here are your results - ")
                Log_Me.info_log(record)
                return record

        except (Exception, Error) as error:
            Log_Me.error_log("Error while connecting to PostgreSQL")
            Log_Me.error_log(error)
            raise error
        finally:
            if connection:
                cursor.close()
                connection.close()
                Log_Me.info_log("PostgreSQL connection is closed")


if __name__ == "__main__":
    DbConn.make_connect("SELECT * FROM application;")
