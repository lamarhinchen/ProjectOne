from time import sleep
from behave import given, when, then
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_playground.features.pages.projectone_home import ProjectOneHome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given(u'I am on the Tuition Reimbursement Profile Page')
def step_impl(context):
    driver: WebDriver = context.driver
    driver.get('C:/Users/Lamar/PycharmProjects/ProjectOne/website/account.html?user=16')


@when(u'I load the Page all work Assigned to me Loads')
def step_impl(context):
    driver: WebDriver = context.driver
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'approve-btn')))


@then(u'I can Approve a Application')
def step_impl(context):
    driver: WebDriver = context.driver
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'approve-btn')))
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_class_name("approve-btn").click()


@then(u'I can Reject an Application')
def step_impl(context):
    driver: WebDriver = context.driver
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'textarea')))
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_tag_name("textarea").send_keys(
        "Hello It's a cruel cruel cruel world, can you buy me a fish?")
    projectone_home.driver.find_element_by_class_name("reject-btn").click()


@then(u'I can request More Information a Application')
def step_impl(context):
    driver: WebDriver = context.driver
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'req-add')))
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_tag_name("textarea").send_keys(
        "Hello It's a cruel cruel cruel world, can you buy me a fish?")
    projectone_home.driver.find_element_by_class_name("req-add").click()


@when(u'I load the Page')
def step_impl(context):
    driver: WebDriver = context.driver
    driver.get('C:/Users/Lamar/PycharmProjects/ProjectOne/website/account.html?user=16')


@then(u'all work Assigned to me Loads')
def step_impl(context):
    driver: WebDriver = context.driver
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'approve-btn')))
