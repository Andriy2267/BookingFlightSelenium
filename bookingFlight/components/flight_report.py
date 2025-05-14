from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class BookingFlightReport:

    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.flight_boxes = self.pull_flight_boxes()

    
    def pull_flight_boxes(self):
        wait = WebDriverWait(self.boxes_section_element, 30)
        flight_boxes = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@data-testid, "searchresults_card")]'))
        )
        print(f"Found {len(flight_boxes)} flight boxes.")
        return flight_boxes
  
    
    def pull_flight_box_attributes(self):
        collection = []
    
        for i, flight_box in enumerate(self.flight_boxes):
            test_ids = [
                "flight_card_carriers",
                "flight_card_carrier_0",
                "flight_card_bound_select_flight"
            ]
            for test_id in test_ids:
                try:
                    carrier_name = flight_box.find_element(By.CSS_SELECTOR, f'div[data-testid="{test_id}"]').text.strip()
                    break
                except NoSuchElementException:
                    continue
            
            try:
                trip_duration_minute = flight_box.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="flight_card_segment_duration_0"]'
                ).text.strip()
            except NoSuchElementException:
                print(f"[{i}] Trip duration not found")
                continue
            
            try:
                shown_price = flight_box.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="flight_card_price_main_price"]'
                ).text.strip()
            except NoSuchElementException:
                print(f"[{i}] Shown price not found")
                shown_price = "N/A"

            try:
                total_price = flight_box.find_element(
                    By.CSS_SELECTOR, 'div[data-testid="flight_card_price_total_price"]'
                ).get_attribute('aria-label').split()[0]
            except NoSuchElementException:
                print(f"[{i}] Total price not found")
                total_price = "N/A"

            try:
                click_button = flight_box.find_element(By.CSS_SELECTOR, 'div[data-testid="flight_card_bound_select_flight"]')
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", click_button)
                click_button.click()
                print(f"[{i}] Clicked select flight button.")
            except Exception as e:
                print(f"[{i}] Could not click select button: {e}")

            collection.append([carrier_name, trip_duration_minute, shown_price, total_price])

        return collection