import time

import booking.constants as const
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# Class Booking inherits class webdriver.Chrome
class Booking(webdriver.Chrome):
    def __init__(self, options=None, teardown=False):
        if options is None:
            options = Options()
            options.add_experimental_option("detach", True)
        self.teardown = teardown
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def close_dialog(self):
        # Wait for the dialog to appear using WebDriverWait
        dialog = WebDriverWait(self, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div[role="dialog"]')
            )
        )
        # Close the dialog by locating the button with specific classes
        if dialog:
            close_button = dialog.find_element(By.CSS_SELECTOR,
                                               'button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.deab83296e.f4552b6561')
            if close_button:
                close_button.click()

    def change_currency(self, currency=None):
        currency_button = self.find_element(By.XPATH, '//button[@data-testid="header-currency-picker-trigger"]')
        currency_button.click()
        currency_overlay = self.find_element(By.XPATH, f'//button[.//div[contains(text(), "{currency}")]]')
        currency_overlay.click()

    def place_to_go(self, place=None):
        search_field = self.find_element(By.XPATH, '//*[@id=":re:"]')
        search_field.clear()
        search_field.send_keys(place)
        time.sleep(1.5)
        first_result = self.find_element(By.XPATH, '//ul[@class="a72ed04875"]/li[1]')
        first_result.click()

    def checkin_date(self, checkindate=None, checkoutdate=None):
        checkin_field = self.find_element(By.XPATH, f'//span[@data-date="{checkindate}"]')
        checkin_field.click()
        checkout_field = self.find_element(By.XPATH, f'//span[@data-date="{checkoutdate}"]')
        checkout_field.click()

    def occupancy_details(self, adults=None, children=None, rooms=None, children_age=None):
        occupancy_field = self.find_element(By.XPATH, '//button[@data-testid="occupancy-config" and @class="d47738b911 b7d08821c3"]')
        occupancy_field.click()

        self.implicitly_wait(3)
        adult_div = self.find_element(By.XPATH, '//div[@class="a7a72174b8"][1]')
        decrease_adult_button = adult_div.find_element(By.XPATH,'.//button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e bb803d8689 e91c91fa93"]')
        adult_count = adult_div.find_element(By.XPATH, './/span[@class="d723d73d5f"]')
        increase_adult_button = adult_div.find_element(By.XPATH, './/button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e bb803d8689 f4d78af12a"]')

        children_div = self.find_element(By.XPATH, '//div[@class="a7a72174b8"][2]')
        children_count = children_div.find_element(By.XPATH, './/span[@class="d723d73d5f"]')
        increase_children_button = children_div.find_element(By.XPATH,'.//button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e bb803d8689 f4d78af12a"]')

        room_div = self.find_element(By.XPATH, '//div[@class="a7a72174b8"][3]')
        room_count = room_div.find_element(By.XPATH, './/span[@class="d723d73d5f"]')
        increase_room_button = room_div.find_element(By.XPATH,'.//button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e bb803d8689 f4d78af12a"]')

        while int(adult_count.text) != 1:
            try:
                decrease_adult_button.click()
            except Exception as e:
                print(e)
                pass
        while int(adult_count.text) != adults:
            try:
                increase_adult_button.click()
            except Exception as e:
                print(e)
                pass
        while int(children_count.text) != children:
            try:
                increase_children_button.click()
            except Exception as e:
                print(e)
                pass
        while int(room_count.text) != rooms:
            try:
                increase_room_button.click()
            except Exception as e:
                print(e)
                pass

        while len(children_age) != 0:
            try:
                self.implicitly_wait(3)
                children_age_field = self.find_element(By.XPATH, f'//div[@data-testid="kids-ages-select"][{len(children_age)}]')
                children_age_field.click()
                children_age_selection = children_age_field.find_element(By.XPATH, f'.//option[@value="{children_age[-1]}"]')
                children_age_selection.click()
                children_age.pop()
            except Exception as e:
                print(e)
                pass

    def search(self):
        search_button = self.find_element(By.XPATH, '//div[@class="f9cf783bde"][4]/button')
        search_button.click()