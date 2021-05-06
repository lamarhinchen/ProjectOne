class AddModel:

    # Data model of Additional information requests

    def __init__(self, info_id=None, from_emp_id=None, to_emp_id=None, app_id=None, urgency_level=None, reason=None,
                 date_received=None, date_completed=None):
        self.info_id = info_id
        self.from_emp_id = from_emp_id
        self.to_emp_id = to_emp_id
        self.app_id = app_id
        self.urgency_level = urgency_level
        self.reason = reason
        self.date_received = date_received
        self.date_completed = date_completed

    def __repr__(self):
        return repr(
            dict(info_id=self.info_id, from_emp_id=self.from_emp_id, to_emp_id=self.to_emp_id, app_id=self.app_id,
                 urgency_level=self.urgency_level, reason=self.reason,
                 date_received=self.date_received, date_completed=self.date_completed))

    def json(self):
        return {
            "Info ID": self.info_id,
            "From Emp ID": self.from_emp_id,
            "To Emp ID": self.to_emp_id,
            "App ID": self.app_id,
            "Urgency": self.urgency_level,
            "Reason": self.reason,
            "Date Started": self.date_received,
            "Completion Date": self.date_completed
        }

    @staticmethod
    def json_parse(json):
        model_of_data = AddModel()
        model_of_data.info_id = json["Info ID"]
        model_of_data.from_emp_id = json["From Emp ID"]
        model_of_data.to_emp_id = json["To Emp ID"]
        model_of_data.app_id = json["App ID"]
        model_of_data.urgency_level = json["Urgency"]
        model_of_data.reason = json["Reason"]
        model_of_data.date_received = json["Date Started"]
        model_of_data.date_completed = json["Completion Date"]

        return model_of_data
