from selenium import webdriver
from utils.logger import configure_logging, get_logger


class UiMethods(object):

    def __init__(self):
        self.driver = webdriver.Chrome()
        configure_logging()
        self.logger = get_logger()
        self.login_btn = '//*[@id="perfect"]/header[1]/div/div[2]/div[3]/ul/li[1]/a'
        self.username_field_id = 'user_login'
        self.password_field_id = 'user_pass'
        self.checkbox_id = 'rememberme'
        self.login_btn_id = 'wp-submit'
        self.error_field_id = 'login_error'

    def quit(self):
        self.logger.info("Trying to close Chrome")
        try:
            self.driver.quit()
        finally:
            self.logger.info("Done closing Chrome")

    def go_to_url(self, url):
        try:
            self.logger.info("Trying to get URL")
            self.driver.get(url)
        except Exception as e:
            raise Exception(f"Desired URL: {url}, exception -  {e}")
        assert self.driver.title.find("404 Page Not Found") < 0, f"URL: {url} results in '404 Page Not Found'"
        assert self.driver.title.find(
            "Problem loading page") < 0, f"URL: {url} results in error 'The page isn't redirecting properly'"

    def go_to_home_page(self):
        self.go_to_url('https://www.brusselstimes.com/')

    def click_login_btn(self):
        self.driver.find_element_by_id(self.login_btn_id).click()

    def go_to_login_page(self):
        self.driver.find_element_by_xpath(self.login_btn).click()

    def enter_username(self, username):
        self.driver.find_element_by_id(self.username_field_id).send_keys(username)

    def enter_password(self, password):
        self.driver.find_element_by_id(self.password_field_id).send_keys(password)

    def check_error_message(self, expected_message):
        error = self.driver.find_element_by_id(self.error_field_id).text
        assert error == expected_message, f'Unexpected message found on page. Expected message: {expected_message}. ' \
                                          f'Actual message: {error}'

    def click_remember_me_checkbox(self):
        self.driver.find_element_by_id(self.checkbox_id).click()
