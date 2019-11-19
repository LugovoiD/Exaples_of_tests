import sys
import inspect
from os.path import join, abspath, dirname
from selenium import webdriver
from utils.logger import configure_logging, get_logger
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC


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

    def get_snapshot(self, filename):
        if self.driver:
            try:
                self.driver.save_screenshot(filename)
            except:
                try:
                    ui.WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                    alert = self.driver.switch_to.alert()
                    self.logger.info(f"Cannot take screenshot. Following alert {alert.text} is present")
                    alert.accept()
                except:
                    pass

    @staticmethod
    def check_test_passed():
        status = {'passed': None, 'skipped': None, 'need_restart': None, 'due': None, 'trace': None}
        trace = sys.exc_info()
        if trace == (None, None, None):
            status['passed'] = True
        elif 'Expected failure' in trace[1].msg:
            status['skipped'] = True
            status['passed'] = True
            status['due'] = trace[1].due
            if trace[1].restart:
                status['need_restart'] = True

        elif 'Unexpected test success' in trace[1].msg:
            status['passed'] = False
            status['need_restart'] = False

        else:
            status['passed'] = False
            status['need_restart'] = True
        return status

    @staticmethod
    def get_test_id():
        stack = inspect.stack()
        for info in stack:
            frame_obj = info[0]
            if frame_obj.f_code.co_name == "__call__":
                found_test_frame = frame_obj
                if 'self' in found_test_frame.f_locals:
                    s = found_test_frame.f_locals['self']
                    test_id = s.id()
                    test_id = test_id.replace("<", "").replace(">", "").replace(" ", "")
                    return test_id

    def get_browser_snapshot_for_test(self, testName=None):
        test_name = testName if testName else self.get_test_id()
        path = abspath(join(dirname(abspath(__file__)), '../'))
        file_name = join(path, f'tests/reports/screens', test_name + '.png')
        if test_name:
            self.get_snapshot(file_name)

    def get_browser_snapshot_if_needed(self):
        if self.check_test_passed()['passed'] is False:
            try:
                self.get_browser_snapshot_for_test()
            finally:
                pass

    def go_to_url(self, url):
        try:
            self.logger.info("Trying to get URL")
            self.driver.get(url)
        except Exception as e:
            self.get_browser_snapshot_if_needed()
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
