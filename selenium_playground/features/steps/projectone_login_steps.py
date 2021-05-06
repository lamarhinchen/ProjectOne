from time import sleep
from behave import given, when, then
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium_playground.features.pages.projectone_home import ProjectOneHome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given(u'I am on the Tuition Reimbursement Home Page')
def get_to_tuition_home_page(context):
    driver: WebDriver = context.driver
    driver.get('C:/Users/Lamar/PycharmProjects/ProjectOne/website/home.html')
    sleep(4)


@when(u'I enter user email as bi in the Search Bar')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.login_bar().send_keys("bi")
    sleep(4)


@when(u'I Click the link for the Email I am looking for')
def click_user_email_link(context):
    driver: WebDriver = context.driver
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'help_email0')))


@then(u'It should route me to the correct User Profile Page')
def login_to_correct_profile(context):
    driver: WebDriver = context.driver
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'help_email0')))
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.login_link().click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be("file:///C:/Users/Lamar/PycharmProjects/ProjectOne/website/account.html?user=10"))


@then(u'It should route me to the correct dept head User Profile Page')
def step_impl(context):
    driver: WebDriver = context.driver
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, 'help_email0')))
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.login_link().click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be("file:///C:/Users/Lamar/PycharmProjects/ProjectOne/website/account.html?user=1"))


@when(u'I enter user email as lam in the Search Bar')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.login_bar().send_keys("lam")
    sleep(4)


@then(u'Dropdown of the search results should appear')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    sleep(4)
    assert projectone_home.login_not_found_res().find_elements_by_tag_name('a')


@when(u'I enter user email as jz in the Search Bar')
def step_impl(context):
    projectone_home: ProjectOneHome = context.projectone_home
    projectone_home.login_bar().send_keys("j")
    sleep(4)
    projectone_home.login_bar().send_keys("z")
    sleep(4)


@then(u'Dropdown of the search should show No employees with this email exist!')
def get_no_results_found(context):
    projectone_home: ProjectOneHome = context.projectone_home
    sleep(4)
    assert projectone_home.login_not_found_res().text == "No employees with this email exist!"
