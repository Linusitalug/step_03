
from myconfiguration import deviceName
from appium import webdriver as driver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.touch_action import TouchAction
import time

wait_time = 0.8

class Myandroid():
    def create_drive(self):
        try:
            des_cap = {

                "platformName": "Android",
                "deviceName": deviceName,
                "newCommandTimeout": 90.000,


            }
            # close notification for whatapp
            self.driver = driver.Remote(command_executor='http://127.0.0.1:4723/wd/hub',
                                        desired_capabilities=des_cap)
            print('driver created success')
            return self.driver
        except Exception as e:
            print(str(e))	
            print('please check that appium server  is running or not')
            exit(0)

    def go_to_home(self):
        print('going to home screen')
        for x in range(1, 10):
            self.driver.back()

    def open_whatsappp(self):
        print('try to find application')
        try:
            xpath = '//android.widget.TextView[@content-desc="WhatsApp1"]'
            xpath = '//android.widget.ImageView[@content-desc="WhatsApp"]'
            wh = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
            wh.click()
        except Exception as e:
            xpath = "//android.widget.TextView[@text='WhatsApp']"
            wh = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
            wh.click()
            print("whatsapp open success")
            time.sleep(wait_time)

