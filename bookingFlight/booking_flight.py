from selenium import webdriver
from bookingFlight.constants import URL_BASE
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from .captcha_solver import solve_funcaptcha

class BookingFlight(webdriver.Chrome):

    def __init__(self, teardown: bool=False, detach: bool=True):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1")
        if detach:
             options.add_experimental_option("detach", True)
 
        service = Service(ChromeDriverManager().install())
        super().__init__(service=service, options=options)
        self.maximize_window()
    

    def __del__(self):
        if self.teardown:
            self.quit()


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()


    def land_first_page(self):
        self.get(URL_BASE)


    def open_flight(self):
        wait = WebDriverWait(self, 5)
        select_fligth_element = wait.until(EC.element_to_be_clickable((By.ID, "flights")))
        select_fligth_element.click()


    def change_language(self, language="English (US)"):
        wait = WebDriverWait(self, 5)
        select_language_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-language-picker-trigger"]')))
        select_language_button.click()

        for language_option in self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]'):
            if language in language_option.text:
                language_option.click()
                break

    
    def change_currency(self, currency="USD"):
        wait = WebDriverWait(self, 5)
        select_currency_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')))
        select_currency_button.click()

        for currency_option in self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]'):
            if currency in currency_option.text:
                currency_option.click()
                break


    def select_flight_type(self, type="One-way"):
        wait = WebDriverWait(self, 5)
        if type == "One-way":
            select_oneway_type = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ui-name="search_type_oneway"]')))
            select_oneway_type.click()
        elif type == "Round-trip":
            select_roundtrip_type = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ui-name="search_type_roundtrip"]')))
            select_roundtrip_type.click()
        else:
            select_multicity_type = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ui-name="search_type_multistop"]')))
            select_multicity_type.click()

    
    def select_flight_option(self, option="Economy"):
        wait = WebDriverWait(self, 5)
        select_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class="Select-module__wrapper___Aa7YD"]')))
        select_option.click()

        if option == "Economy":
            select_economy_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'option[value="ECONOMY"]')))
            select_economy_option.click()
        elif option == "Premium economy":
            select_premiumeconomy_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'option[value="PREMIUM_ECONOMY"]')))
            select_premiumeconomy_option.click()
        elif option == "Business":
            select_business_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'option[value="BUSINESS"]')))
            select_business_option.click()
        else:
            select_firstclass_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'option[value="FIRST"]')))
            select_firstclass_option.click()

    
    def select_direct_flight(self, direct_flight=True):
        wait = WebDriverWait(self, 5)
        if direct_flight:
            select_direct_flight = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ui-name="direct_flights"]')))
            select_direct_flight.click()




                

                                          

    