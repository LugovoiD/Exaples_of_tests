import unittest
import nose2
from utils.ui_methods import UiMethods
from ddt import ddt, data

# This is a test suite only with negative tests because "The Brussels Times" site
# gives permission for login only for administrators


@ddt
class TestsLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = UiMethods()
        super(TestsLogin, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.go_to_home_page()

    def test_01_login_without_properties(self):
        self.driver.go_to_login_page()
        self.driver.click_login_btn()
        self.driver.check_error_message("Error: The username field is empty.")

    @data('Test_name', 'testmail@gmail.com')
    def test_02_enter_only_name(self, username):
        self.driver.go_to_login_page()
        self.driver.enter_username(username)
        self.driver.click_login_btn()
        self.driver.check_error_message("Error: The password field is empty.")

    def test_03_enter_only_password(self):
        self.driver.go_to_login_page()
        self.driver.enter_password('password')
        self.driver.click_login_btn()
        self.driver.check_error_message("Error: The username field is empty.")

    def test_04_enter_username_and_password(self):
        self.driver.go_to_login_page()
        self.driver.enter_username('username')
        self.driver.enter_password('password')
        self.driver.click_login_btn()
        self.driver.check_error_message("Error: Invalid Username.")

    def test_05_login_with_email(self):
        self.driver.go_to_login_page()
        self.driver.enter_username('testmail@gmail.com')
        self.driver.enter_password('password')
        self.driver.click_login_btn()
        self.driver.check_error_message("Error: The email address isn't correct..")


if __name__ == "__main__":
    nose2.main()
