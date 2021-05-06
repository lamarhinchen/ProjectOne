from time import sleep
from behave import given, when, then
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_playground.features.pages.projectone_home import ProjectOneHome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@when(u'I type my email in the search bar')
def step_impl(context):
    driver: WebDriver = context.driver
    driver.get('C:/Users/Lamar/PycharmProjects/ProjectOne/website/home.html')
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.app_login_bar().send_keys("bil")
    sleep(4)


@then(u'My full email shows underneath as a link')
def step_impl(context):
    driver: WebDriver = context.driver
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "billjamerson@revature.net")))


@when(u'I click the email link')
def step_impl(context):
    driver: WebDriver = context.driver
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'help_email0')))


@then(u'My First, Middle, and Last name Load into their respective fields')
def step_impl(context):
    driver: WebDriver = context.driver
    driver.get('C:/Users/Lamar/PycharmProjects/ProjectOne/website/application.html?user=10')
    projectone_home: ProjectOneHome = context.projectone_home
    sleep(4)
    assert projectone_home.driver.find_element_by_id("firstname").get_attribute("value") == "bill"
    assert projectone_home.driver.find_element_by_id("middlename").get_attribute("value") == "stein"
    assert projectone_home.driver.find_element_by_id("lastname").get_attribute("value") == "jamerson"


@given(u'I am on the Tuition Reimbursement Application Page')
def step_impl(context):
    driver: WebDriver = context.driver
    driver.get('C:/Users/Lamar/PycharmProjects/ProjectOne/website/application.html?user=10')


@when(u'I try to submit the application before all required fields were completed')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_id("sub_app").get_attribute("disabled")


@then(u'Nothing happens')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    assert projectone_home.driver.title == "Submit Application"


@when(u'I complete the form correctly')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_id("address").send_keys("smith street")
    projectone_home.driver.find_element_by_id("city").send_keys("hampton")
    projectone_home.driver.find_element_by_id("state").send_keys("ohio")
    projectone_home.driver.find_element_by_id("zip").send_keys(12345)
    projectone_home.driver.find_element_by_id("description").send_keys(
        "I just love submitting things over and over and over again!")
    projectone_home.driver.find_element_by_id("work_just").send_keys(
        "I just love submitting things over and over and over again!")
    projectone_home.driver.find_element_by_id("price_tag").send_keys(100)
    projectone_home.driver.find_element_by_id("missed_time").send_keys(100)
    projectone_home.driver.find_element_by_id("date_event").send_keys("5/21/2021")


@then(u'The submit button becomes enabled')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_id("sub_app").get_attribute("disabled")


@when(u'I input a negative value in a number field')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_id("zip").send_keys(-1)


@then(u'The field should auto correct itself to one')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.driver.find_element_by_id("zip").send_keys(1)
