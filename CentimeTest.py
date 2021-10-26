from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import logging,unittest
import random,string
from selenium.webdriver.common.action_chains import ActionChains


class handywrappers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        email_generator = lambda: (''.join(random.choice(string.ascii_letters) for x in range(10))) + "@gmail.com"
        cls.email = email_generator()


    def setUp(self):
        self.driver = webdriver.Chrome("C:\ChromeDriver\chromedriver")
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()
        self.base_url = "http://automationpractice.com/index.php"
        self.driver.get(self.base_url)
        time.sleep(10)


    def tearDown(self):
        self.driver.quit()

    def getByType(self,locatorType):
        locatorType = locatorType.lower()

        if locatorType == "id":
            return By.ID

        elif locatorType == "xpath":
            return By.XPATH

        elif locatorType == "name":
            return By.NAME

        elif locatorType == "css":
            return By.CSS_SELECTOR

        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link_text":
            return By.LINK_TEXT
        elif locatorType == "xpath":
            return By.XPATH

        else:
            print("Locator type is not supported")

        return False

    def getElement(self,locator,locatorType):
        element = None

        try:
            locatorType = locatorType.lower()
            ByType = self.getByType(locatorType)
            element = self.driver.find_element(ByType,locator)
        except:
            # logging.error("Either element is not found or you are not in correct page")
            return False
        return element

    def click_and_send_value(self,locator,locatorType,value=None):

        field = self.getElement(locator,locatorType)
        field.click()
        field.clear()
        time.sleep(2)
        field.send_keys(value)
        time.sleep(2)
        return

    # def Email_generator(self):
    #     return (''.join(random.choice(string.ascii_letters) for x in range(10))) + "@gmail.com"


    def fill_details(self,Gender,FN = None,LN = None,Email = None,Company= None,Address=None,City=None):
        First_Name = self.click_and_send_value("customer_firstname","id",FN)
        Last_Name = self.click_and_send_value("customer_lastname","id",LN)
        Email = self.click_and_send_value("email","id",Email)
        Password = self.click_and_send_value("passwd","id","12345678")

        Date = self.getElement("days","id")
        sel = Select(Date)
        sel.select_by_index("10")

        Month  = self.getElement("months","id")
        sel = Select(Month)
        sel.select_by_index("11")

        Year = self.getElement("years","id")
        sel = Select(Year)
        sel.select_by_index("20")

        time.sleep(2)

        FirstName = self.click_and_send_value("firstname","id",FN)
        LastName = self.click_and_send_value("lastname","id",LN)
        Company = self.click_and_send_value("company","id",Company)
        Address = self.click_and_send_value("address1","id",Address)
        City = self.click_and_send_value("city","id",City)
        State = self.getElement("id_state","id")
        sel = Select(State)
        sel.select_by_index("10")

        PostalCode = self.click_and_send_value("postcode","id","81530")
        HomePhone = self.click_and_send_value("phone","id","123456789")
        MobilePhone = self.click_and_send_value("phone_mobile","id","987654321")
        time.sleep(5)

    def Create_An_Account(self,Gender,FN = None,LN = None,Email = None,Company= None,Address=None,city=None):

        try:
            locator = "email_create"
            Login = self.getElement("login","Class")
            Login.click()
            time.sleep(5)

            self.click_and_send_value(locator, locatorType="id", value=Email)
            Create_An_Account = self.getElement("SubmitCreate", "id")

            Create_An_Account.click()
            time.sleep(5)
            self.fill_details(Gender, FN, LN, Email, Company, Address, city)
            RegisterButton = self.getElement("submitAccount", "id")
            RegisterButton.click()
            time.sleep(10)

        except:
            # print("This email address already exists.Please try with another email id")
            return False
        return True

    def Login(self,email = None, Password = None):

        try:
            Login = self.getElement("login", "Class")
            Login.click()
            time.sleep(5)
            Email_Address = self.click_and_send_value("email", "id", email)
            Password = self.click_and_send_value("passwd", "id", Password)

            time.sleep(2)
            Sign_in = self.getElement("SubmitLogin", "id")
            Sign_in.click()
            time.sleep(2)
        except:
            # logging.error("Credential is incorrect. Please try with correct credential")
            return False
        return True

    def test_a_Registration_with_blank_mandatory_field(self):
        print("\nTest Case :" + self._testMethodName)
        print("*********************************************************")
        expected_url = "http://automationpractice.com/index.php?controller=my-account"
        test =  self.Create_An_Account("M",FN = "",LN="", Email=self.email, Company="Centime",
                                       Address="Jharkhand", city="Giridih")
        actual_url = self.driver.current_url

        if self.assertNotEqual(actual_url,expected_url) is not True:
            print("Test Passed")

    def test_b_Registration_with_new_email(self):
        print("\nTest Case :" + self._testMethodName)
        print("***************************************************")
        expected_url = "http://automationpractice.com/index.php?controller=my-account"
        test = self.Create_An_Account("M","Ranjan","Kumar",Email = self.email,Company="Centime",Address="Jharkhand",city="Giridih")

        actual_url = self.driver.current_url
        if self.assertEqual(actual_url,expected_url) is not True:
            print("Test Passed")

    def test_c_Registration_with_existing_email(self):
        print("\nTest Case :" + self._testMethodName)
        print("*******************************************************")
        expected_url = "http://automationpractice.com/index.php?controller=authentication&back=my-account#account-creation"
        test = self.Create_An_Account("M","Ranjan","Kumar",Email = self.email,Company="Centime",Address="Jharkhand",city="Giridih")
        actual_url = self.driver.current_url

        if self.assertNotEqual(actual_url,expected_url) is not True:
            print("Test Passed")


    def test_d_Login_with_correct_credential(self):
        print("\nTest Case :" + self._testMethodName)
        print("*****************************************************")
        expected_url = "http://automationpractice.com/index.php?controller=my-account"
        test = self.Login(email = self.email,Password = "12345678")

        actual_url = self.driver.current_url

        if self.assertEqual(actual_url,expected_url) is not True:
            print("Test Passed")

    def test_e_Login_with_incorrect_credential(self):
        print("\nTest Case :" + self._testMethodName)
        print("*****************************************************")
        expected_url = "http://automationpractice.com/index.php?controller=my-account"
        test = self.Login(email = self.email,Password = "1234567")

        actual_url = self.driver.current_url

        if self.assertNotEqual(actual_url,expected_url) is not True:
            print("Test Passed")

    def test_f_cart_testing(self):
        print("\nTest Case :" + self._testMethodName)
        print("*****************************************************")
        Login = self.Login("ranjan13jms@gmail.com",Password="12345678")
        actual_cart_count = 0
        Dresses = self.driver.find_element(By.XPATH,"//ul[@class='sf-menu clearfix menu-content sf-js-enabled sf-arrows']/li[2]")
        Dresses.click()
        time.sleep(5)
        items = self.driver.find_elements(By.CLASS_NAME,"ajax_block_product")
        Add_to_cart = self.getElement("//div[@class = 'button-container']/a[@title = 'Add to cart']","Xpath")

        action = ActionChains(self.driver)
        for item in items:
            item.location_once_scrolled_into_view
            action.move_to_element(item).perform()
            time.sleep(5)
            action.click(Add_to_cart).click().perform()
            actual_cart_count+=1
            time.sleep(2)
            self.driver.back()

        expected_Cart_Count = self.getElement("ajax_cart_quantity","Class").text
        self.assertEqual(actual_cart_count,expected_Cart_Count)

if __name__=="__main__":
    unittest.main()





