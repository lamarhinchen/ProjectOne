class EmpModel:

    # Data model of Employees

    def __init__(self, emp_id=None, firstname=None, middlename=None, lastname=None, email=None, disabled=None,
                 date_employed=None, date_terminated=None):
        self.emp_id = emp_id
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.email = email
        self.disabled = disabled
        self.date_employed = date_employed
        self.date_terminated = date_terminated

    def __repr__(self):
        return repr(dict(emp_id=self.emp_id, firstname=self.firstname, lastname=self.lastname))

    def json(self):
        return {
            "Employee ID": self.emp_id,
            "First Name": self.firstname,
            "Middle Name": self.middlename,
            "Last Name": self.lastname,
            "Email": self.email,
            "Not Employed?": self.disabled,
            "Employment Date": self.date_employed,
            "Termination Date": self.date_terminated
        }

    @staticmethod
    def json_parse(json):
        model_of_data = EmpModel()
        model_of_data.emp_id = json["Employee ID"]
        model_of_data.firstname = json["First Name"]
        model_of_data.middlename = json["Middle Name"]
        model_of_data.lastname = json["Last Name"]
        model_of_data.email = json["Email"]
        model_of_data.disabled = json["Not Employed?"]
        model_of_data.date_employed = json["Employment Date"]
        model_of_data.date_terminated = json["Termination Date"]

        return model_of_data
