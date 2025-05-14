from selenium import webdriver
from bookingFlight.constants import URL_BASE
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from .captcha_solver import solve_funcaptcha
from selenium.common.exceptions import StaleElementReferenceException
from .components.flight_report import BookingFlightReport

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
    

    def close_optional_popup(self):
        try:
            popup = WebDriverWait(self, 3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "bbe73dce14"))
            )
            try:
                close_button = popup.find_element(By.CSS_SELECTOR, 'span[class="ec1ff2f0cb"]')
                close_button.click()
            except NoSuchElementException:
                WebDriverWait(self, 5).until(
                    EC.invisibility_of_element_located((By.CLASS_NAME, "bbe73dce14"))
                )
        except TimeoutException:
            pass

    
    def change_currency(self, currency="USD"):
        wait = WebDriverWait(self, 5)
        select_currency_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')))
        select_currency_button.click()

        for currency_option in self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]'):
            if currency in currency_option.text:
                currency_option.click()
                break


    def select_flight_type(self, type="Round-trip"):
        wait = WebDriverWait(self, 10)

        type_selectors = {
            "One-way": 'div[data-ui-name="search_type_oneway"]',
            "Round-trip": 'div[data-ui-name="search_type_roundtrip"]',
            "Multi-city": 'div[data-ui-name="search_type_multistop"]'
        }

        selector = type_selectors.get(type, type_selectors["One-way"])  
        flight_type_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        flight_type_element.click()

    
    def select_flight_option(self, option="Economy"):
        wait = WebDriverWait(self, 5)
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class="Select-module__wrapper___Aa7YD"]')))
        dropdown.click()

        option_values = {
            "Economy": "ECONOMY",
            "Premium economy": "PREMIUM_ECONOMY",
            "Business": "BUSINESS",
            "First": "FIRST"
        }

        value = option_values.get(option, "ECONOMY")
        option_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'option[value="{value}"]')))
        option_element.click()

    
    def select_direct_flight(self, direct_flight=True):
        wait = WebDriverWait(self, 5)
        if direct_flight:
            select_direct_flight = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-ui-name="direct_flights"]')))
            select_direct_flight.click()

    
    def select_outbound_flight(self, origin_flight="LHR", destination_flight="FRA"):
        wait = WebDriverWait(self, 25)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-ui-name="input_location_from_segment_0"]'))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'span[class="Chip-module__trigger___6n8tM"]'))).click()

        input_origin = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="AutoComplete-module__textInput___Qh3I- "]')))
        input_origin.clear()
        input_origin.send_keys(origin_flight)

        suggestion_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul#flights-searchbox_suggestions li')))

        for item in suggestion_list:
            if origin_flight in item.text:
                item.click()
                break

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-ui-name="input_location_to_segment_0"]'))).click()
        input_destionation = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="AutoComplete-module__textInput___Qh3I- "]')))
        input_destionation.clear()
        input_destionation.send_keys(destination_flight)

        suggestion_dest_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul#flights-searchbox_suggestions li')))
        
        for item in suggestion_dest_list:
            if destination_flight in item.text:
                item.click()
                break

        
    def select_oneway_flight_date(self, checkin="2025-06-20"):
        wait = WebDriverWait(self, 20)

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-ui-name="button_date_segment_0"]'))).click()

        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{checkin}"]'))).click()

    
    def select_flight_occupancy(self, adults: int = 1, children: int = 0, children_ages: list[int] = None):
        wait = WebDriverWait(self, 10)

        occupancy_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-ui-name="button_occupancy"]')))
        occupancy_button.click()

        adult_plus_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-ui-name="button_occupancy_adults_plus"]')))
        adult_minus_button = self.find_element(By.CSS_SELECTOR,
            'button[data-ui-name="button_occupancy_adults_minus"]')

        adult_value = int(self.find_element(By.CSS_SELECTOR,
            'div[data-ui-name="occupancy_adults"] span.InputStepper-module__value___gCdYu').text)

        while adult_value < adults:
            adult_plus_button.click()
            adult_value += 1
        while adult_value > adults:
            adult_minus_button.click()
            adult_value -= 1

        ## Children
        child_plus_button = self.find_element(By.CSS_SELECTOR, 'button[data-ui-name="button_occupancy_children_plus"]')
        child_minus_button = self.find_element(By.CSS_SELECTOR, 'button[data-ui-name="button_occupancy_children_minus"]')

        child_value = int(self.find_element(By.CSS_SELECTOR,
            'div[data-ui-name="occupancy_children"] span.InputStepper-module__value___gCdYu').text)

        while child_value < children:
            child_plus_button.click()
            child_value += 1
        while child_value > children:
            child_minus_button.click()
            child_value -= 1

        ## Choose children age
        if children > 0:
            if not children_ages or len(children_ages) != children:
                raise ValueError("You must provide a list of ages for each child.")

            for i in range(children):
                age_select = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f'select[name="sr_occupancy_children_age_{i}"]')))
                Select(age_select).select_by_value(str(children_ages[i]))

        ## Button "Done"
        done_button = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button[data-ui-name="button_occupancy_action_bar_done"]')))
        done_button.click()


    def select_search_button(self):
        wait = WebDriverWait(self, 10)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-ui-name="button_search_submit"]'))).click()

    
    def select_BCF_flight(self, flight_rate: str = "Cheapest"):
        wait = WebDriverWait(self, 30)

        valid_options = {"BEST", "CHEAPEST", "FASTEST"}
        rate_upper = flight_rate.upper()

        if rate_upper not in valid_options:
            raise ValueError(f"Invalid flight_rate '{flight_rate}'. Must be one of: {', '.join(valid_options)}")
        
        try:
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '[class^="modal-module__overlay___"]')))
        except:
            pass

        tab_locator = (By.CSS_SELECTOR, f'button[data-testid="search_tabs_{rate_upper}"]')

        for attempt in range(3):
            try:
                wait.until(lambda driver: driver.find_element(*tab_locator).is_enabled() and driver.find_element(*tab_locator).click() is None)
                break
            except StaleElementReferenceException:
                continue


    def report_results(self):
        wait = WebDriverWait(self, 40)
        flight_boxes = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[tabindex="0"]')))
        report = BookingFlightReport(flight_boxes)
        print(report.pull_flight_box_attributes())






        
        

    





                

                                          

    