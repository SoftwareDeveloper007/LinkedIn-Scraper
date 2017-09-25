from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import threading, time, csv, xlrd, os, sys, platform

def takeFirst(elem):
    return elem[0]

email = 'qingxin_age@hotmail.com'
password = 'passion1989'

class mainScraper():
    def __init__(self, search_word):

        self.search_word = search_word
        self.output_data = []

    def startScraping(self):

        self.driver = webdriver.Chrome(os.getcwd() + '/WebDriver/chromedriver.exe')
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/m/login/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))


        signin = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "p.signin-link > a"))
        )
        signin.click()

        id = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#session_key-login"))
        )
        pswd = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#session_password-login"))
        )

        id.send_keys(email)
        pswd.send_keys(password)

        time.sleep(1)
        btn = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#btn-primary"))
        )

        btn.click()

        time.sleep(1)
        #print(self.driver.page_source)
        search_in = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.type-ahead-input-container > div > div > input"))
        )

        search_in.click()
        time.sleep(1)

        self.driver.refresh()

        search_in = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.type-ahead-input-container > div > div > input"))
        )

        action_chain = ActionChains(self.driver)
        action_chain \
            .click(search_in) \
            .key_down(Keys.CONTROL) \
            .send_keys('a') \
            .key_up(Keys.CONTROL) \
            .send_keys(Keys.DELETE) \
            .send_keys(self.search_word) \
            .send_keys(Keys.ENTER) \
            .perform()

        people_tab = WebDriverWait(self.driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.neptune-grid.two-column > ul"))
        )

        people_tab.find_elements_by_tag_name('li')[1].find_element_by_tag_name('button').click()

        #self.driver.find_element_by_css_selector('li.search-facet.search-facet--current-company > button > span > span > h3').click()

        current_company = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.search-facet.search-facet--current-company > button"))
        )
        current_company.click()

        self.driver.find_element_by_css_selector('li.search-facet.search-facet--current-company').find_elements_by_tag_name('li')[0].click()
        print(self.driver.find_element_by_css_selector(
            'li.search-facet.search-facet--current-company').find_elements_by_tag_name('li')[0].text)
        print('OK')

if __name__ == '__main__':
    app = mainScraper('Duo Security')
    app.startScraping()