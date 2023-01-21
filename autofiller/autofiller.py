from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class AutoFiller:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        chrome_driver = '/chromdriver_mac/chromedriver'

        # Debug using below
        # driver = webdriver.Chrome(chrome_driver)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def send_pass(self, str):
        password = self.driver.find_element(By.XPATH, "//input[@type='password']")
        password.send_keys(str)