from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
import re

class BookingFlightReport:

    def __init__(self, driver: WebDriver, boxes_section_element: WebElement):
        self.driver = driver
        self.boxes_section_element = boxes_section_element
        self.flight_boxes = self.pull_flight_boxes()

    
    def pull_flight_boxes(self):
        wait = WebDriverWait(self.driver, 30)
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
                view_btn = WebDriverWait(self.driver, 25).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='flight_card_bound_select_flight']")))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_btn)
                view_btn.click()

                modal = WebDriverWait(self.driver, 25).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
                )

                try:
                    cabin_class_element = modal.find_element(By.CSS_SELECTOR, 'div[data-testid="timeline_leg_info_flight_number_and_class"]')
                    raw_text = cabin_class_element.text.strip()

                    try:
                        flight_no_raw, cabin_class = map(str.strip, raw_text.split("·"))
                        # Formating flight_no: BA902 -> BA-902
                        match = re.match(r"([A-Z]+)(\d+)", flight_no_raw)
                        if match:
                            flight_no = f"{match.group(1)}-{match.group(2)}"
                        else:
                            flight_no = flight_no_raw  

                    except ValueError:
                        print(f"[{i}] Unexpected cabin_class format: {raw_text}")
                        flight_no = "N/A"
                        cabin_class = "N/A"

                except NoSuchElementException:
                    print(f"[{i}] Cabin class not found inside modal")
                    cabin_class = "N/A"
                    flight_no = "N/A"

                # Close modal window
                close_btn = modal.find_element(By.CSS_SELECTOR, 'button[class="Actionable-module__root___R7KVb Button-module__root___fc6ts Button-module__root--variant-tertiary___h3ti4 Button-module__root--icon-only___9nJ1C Button-module__root--size-medium___AhzfB Button-module__root--variant-tertiary-neutral___IHuoF"]').click()

                WebDriverWait(self.driver, 25).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, "[role='dialog']"))
                )

            except TimeoutException:
                print("Timeout waiting for modal or elements. Пропускаємо цей рейс.")
            except Exception as e:
                print(f"Помилка при обробці flight_box: {e}")
                continue

            collection.append([carrier_name, trip_duration_minute, shown_price, total_price, cabin_class, flight_no])

        return collection