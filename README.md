# Tuition Reimbursement Management System (TRMS)

## Project Description
The purpose of TRMS is to provide a system that encourages quality knowledge growth relevant to an individual’s expertise.   Currently, TRMS provides reimbursements for university courses, seminars, certification preparation classes, certifications, and technical training.  The current system relies solely on email communication, requiring manual lookups of available funds and is error-prone due to inbox clutter and incorrect routing of tasks.  Furthermore, there is no way to record and report on reimbursements awarded, and so the company has no way to identify highly-invested courses that could be developed to be offered in-house.

## Technologies Used:

* Python version 3.9
* Bootstrap vesion 4.3.1
* JavaScript version ES6.0(ECMAScript 2018)
* HTML version 5.0
* CSS version 3.0
* Cucumber version 3.0
* Behave version 1.2.6
* click version 7.1.2
* Flask version 1.1.2
* Flask-Cors version 3.0.10
* itsdangerous version 1.1.0
* Jinja2 version 2.11.3
* MarkupSafe version 1.1.1
* parse version 1.19.0
* parse-type version 0.5.2
* pip version 21.1.1
* psycopg2 version 2.8.6
* selenium version 3.141.0
* setuptools version 49.2.1
* six version 1.16.0
* style version 1.1.0
* update version 0.0.1
* urllib3 version 1.26.4
* Werkzeug version 1.0.1

## Features

List of features ready and TODOs for future development
* Each employee is allowed to claim up to $1000 in tuition reimbursement a year.  The amount available to an employee is reset on the new year.  Event types have different standard reimbursement coverage: University Courses 80%, Seminars 60%, Certification Preparation Classes 75%, Certification 100%, Technical Training 90%, Other 30%.  After a BenCo has approved a reimbursement, the reimbursement is pending until a passing grade or presentation over the event is provided.  The monetary amount available for an employee to reimburse is defined by the following equation: AvailableReimburstment = TotalReimburstment ($1000) – PendingReimburstments – AwardedReimburstments.  If the projected reimbursement for an event exceeds the available reimbursement amount, it is adjusted to the amount available.  Reimbursements do not cover course materials such as books.
* All Employees must complete the Tuition Reimbursement form one week prior to the start of the event.  This form must collect (required): basic employee information; date, time, location, description, cost, grading format, and type of event; work-related justification.  The employee can optionally include: event-related attachments of pdf, png, jpeg, txt, or doc file type, attachments of approvals already provided of .msg (Outlook Email File) file type and type of approval, work time that will be missed.  The projected reimbursement should be provided as a read-only field.
* Grading formats are pulled from a reference table.  Certain grading formats require the employee to perform a presentation to management after the event’s completion and prior to awarded reimbursement.  A passing grade is needed for reimbursement otherwise.  Employee must provide the passing grade cutoff for the course, or choose to use a default passing grade if unknown.  If an employee provides an approval email, that approval step is skipped (cannot skip BenCo Approval).  If the course is < 2 weeks from beginning, the request is marked urgent.
* The direct supervisor must provide approval for Tuition Reimbursement.  The Direct Supervisor can request additional information from the employee before approval. 
* If denied, the Direct Supervisor must provide a reason.  If the direct supervisor is also a department head, then the department head approval is skipped.  If the direct supervisor does not complete this task in a timely matter, the request is auto-approved. 
* The department head must provide approval for Tuition Reimbursement.  The Department Head can request additional information from the employee or direct supervisor before approval.
* If the Department Head does not complete this task in a timely matter, the request is auto-approved.
* The BenCo must provide approval for Tuition Reimbursement.   This stage is not skippable for any reason.  The BenCo can request additional information from the employee, direct supervisor, or department head before approval. The BenCo has the ability to alter the reimbursement amount.
* Only interested parties are able to access the grades/presentations.  Interested parties include the requestor and approvers.

To-do list:
* Add message system that sends email to management for notifications
* have the uploaded files complile into a viewable pdf and send the documents in an email with notifications

## Getting Started
   
(must have software like(Pycharm) to run python)

> Compatible with all systems

- Run main.py

## Usage

> Run the flask instance from main.py so the endpoints exist.
> Navigate to the homepage and start to type letters to mock a current employee. It will autofill with the existing email and then click the email of the employee you wish to mock. You do this to login or go the fill out the form page.

## License

This project uses the following license: [<GPL-3.0 License>](<https://github.com/lamarhinchen/ProjectOne/blob/main/LICENSE>).
