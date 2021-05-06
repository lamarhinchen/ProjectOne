class WorkListModel:

    # Data model of applications

    def __init__(self, work_id=None, emp_id=None, app_id=None, urgency_level=None, description=None, approval=None,
                 date_received=None, date_completed=None):
        self.work_id = work_id
        self.emp_id = emp_id
        self.app_id = app_id
        self.urgency_level = urgency_level
        self.description = description
        self.approval = approval
        self.date_received = date_received
        self.date_completed = date_completed

    def __repr__(self):
        return repr(dict(app_id=self.app_id, emp_id=self.emp_id, work_id=self.work_id))

    def json(self):
        return {
            "Work ID": self.work_id,
            "Employee ID": self.emp_id,
            "Application ID": self.app_id,
            "Urgency level": self.urgency_level,
            "Description": self.description,
            "Approved": self.approval,
            "Date Received": self.date_received,
            "Date Completed": self.date_completed
        }

    @staticmethod
    def json_parse(json):
        tuition_app_data = WorkListModel()
        tuition_app_data.work_id = json["Work ID"]
        tuition_app_data.emp_id = json["Employee ID"]
        tuition_app_data.app_id = json["Application ID"]
        tuition_app_data.urgency_level = json["Urgency level"]
        tuition_app_data.description = json["Description"]
        tuition_app_data.approval = json["Approved"]
        tuition_app_data.date_received = json["Date Received"]
        tuition_app_data.date_completed = json["Date Completed"]

        return tuition_app_data
