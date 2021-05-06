class AppModel:

    # Data model of applications

    def __init__(self, app_id=None, emp_id=None, address=None, address_second=None, city=None, state=None, zipcode=None,
                 description=None, work_just=None, price_tag=None, refunded_amt=None, event_types=None,
                 grade_format=None,
                 sup_approval_attach=None, sup_approval=None, dept_approval=None, benco_approval=None,
                 date_received=None, date_event=None, missed_time=None, min_grade=None):
        self.app_id = app_id
        self.emp_id = emp_id
        self.address = address
        self.address_second = address_second
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.description = description
        self.work_just = work_just
        self.price_tag = float(price_tag)
        self.refunded_amt = float(refunded_amt)
        self.event_types = event_types
        self.grade_format = grade_format
        self.sup_approval_attach = sup_approval_attach
        self.sup_approval = sup_approval
        self.dept_approval = dept_approval
        self.benco_approval = benco_approval
        self.date_received = date_received
        self.date_event = date_event
        self.missed_time = float(missed_time)
        self.min_grade = min_grade

    def __repr__(self):
        return repr(
            dict(app_id=self.app_id, emp_id=self.emp_id, price_tag=self.price_tag, refunded_amt=self.refunded_amt,
                 event_types=self.event_types, sup_approval_attach=self.sup_approval_attach,
                 sup_approval=self.sup_approval, dept_approval=self.dept_approval, benco_approval=self.benco_approval,
                 date_event=self.date_event))

    def json(self):
        return {
            "Application ID": self.app_id,
            "Employee ID": self.emp_id,
            "Address": self.address,
            "Second Address": self.address_second,
            "City": self.city,
            "State": self.state,
            "Zip Code": self.zipcode,
            "Description": self.description,
            "Justification": self.work_just,
            "Total Cost": self.price_tag,
            "Total Refunded": self.refunded_amt,
            "Event Type": self.event_types,
            "Grading Format": self.grade_format,
            "Supervisor Attached Approval": self.sup_approval_attach,
            "Supervisor Approval": self.sup_approval,
            "Department Head Approval": self.dept_approval,
            "Benefits Coordinator Approval": self.benco_approval,
            "File Date": self.date_received,
            "Event Date": self.date_event,
            "Missed Time": self.missed_time,
            "Grade Scale": self.min_grade
        }

    @staticmethod
    def json_parse(json):
        tuition_app_data = AppModel()
        tuition_app_data.app_id = json["Application ID"]
        tuition_app_data.emp_id = json["Employee ID"]
        tuition_app_data.address = json["Address"]
        tuition_app_data.address_second = json["Second Address"]
        tuition_app_data.city = json["City"]
        tuition_app_data.state = json["State"]
        tuition_app_data.zipcode = json["Zip Code"]
        tuition_app_data.description = json["Description"]
        tuition_app_data.work_just = json["Justification"]
        tuition_app_data.price_tag = json["Total Cost"]
        tuition_app_data.refunded_amt = json["Total Refunded"]
        tuition_app_data.event_types = json["Event Type"]
        tuition_app_data.grade_format = json["Grading Format"]
        tuition_app_data.sup_approval_attach = json["Supervisor Attached Approval"]
        tuition_app_data.sup_approval = json["Supervisor Approval"]
        tuition_app_data.dept_approval = json["Department Head Approval"]
        tuition_app_data.benco_approval = json["Benefits Coordinator Approval"]
        tuition_app_data.date_received = json["File Date"]
        tuition_app_data.date_event = json["Event Date"]
        tuition_app_data.missed_time = json["Missed Time"]
        tuition_app_data.min_grade = json["Grade Scale"]

        return tuition_app_data
