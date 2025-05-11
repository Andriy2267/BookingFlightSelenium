from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bookingFlight.constants import URL_BASE
from bookingFlight.pages.home_page import HomePage
from bookingFlight.pages.flight_search_page import FlightSearchPage
from .captcha_solver import solve_funcaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BookingFlight(webdriver.Chrome):

    def __init__(self, teardown: bool=False, detach: bool=True):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1")
        if detach:
            options.add_experimental_option("detach", True)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def __del__(self):
        if self.teardown:
            self.driver.quit()

    def land_first_page(self):
        self.driver.get(URL_BASE)

    def search_flight(self, origin="LHR", destination="FRA"):
        homepage = HomePage(self.driver)
        homepage.go_to_flights()
        flight_page = FlightSearchPage(self.driver)
        flight_page.select_route(origin, destination)

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

    def quit(self):
        if self.teardown:
            self.driver.quit()
