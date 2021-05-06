from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.projectone_home import ProjectOneHome


def before_all(context):
    driver: WebDriver = webdriver.Chrome("C:/Users/Lamar/PycharmProjects/chromedriver_win32/chromedriver.exe")
    projectone_home = ProjectOneHome(driver)

    context.driver = driver
    context.projectone_home = projectone_home
    print("started")


def after_all(context):
    context.driver.close()
    context.driver.quit()
    print("ended")
