from selenium.webdriver.chrome.webdriver import WebDriver


class ProjectOneHome:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def login_bar(self):
        return self.driver.find_element_by_id('my_search')

    def login_link(self):
        return self.driver.find_element_by_id('help_email0')

    def app_login_bar(self):
        return self.driver.find_element_by_id('my_search2')

    def app_login_link(self):
        return self.driver.find_element_by_id('load_emails2')

    def login_not_found_res(self):
        return self.driver.find_element_by_id("email_container")
