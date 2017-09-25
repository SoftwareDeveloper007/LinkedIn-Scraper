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
        self.base_url = ''

    def startScraping(self):

        self.driver = webdriver.Chrome(os.getcwd() + '/WebDriver/chromedriver.exe')
        self.driver.maximize_window()
        self.driver.get('https://www.linkedin.com/m/login/')
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))

        '''
        signin = WebDriverWait(self.driver, 200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "p.signin-link > a"))
        )
        signin.click()
        '''
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

        self.base_url = self.driver.current_url

        page_index = 0
        while 1:
            if 'No results found.' not in self.driver.find_element_by_tag_name('html').text.strip():
                page_index += 1     # If 'No results found' is not in the page text, increase the page number
            else:
                # If 'No results found' is in the page text, break from while loop
                break

            # If page number is greater than 1, create next page url
            if page_index > 1:
                self.driver.get(self.base_url + '&page={}'.format(page_index))

            '''
            total_result = WebDriverWait(self.driver, 200).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-results")))

            rows = WebDriverWait(total_result, 200).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.search-result")))
            '''

            time.sleep(5)


            #for row in rows:
            for _i in range(10):
                # Rows in the first page
                rows = WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-results")))
                #rows = self.driver.find_element_by_css_selector('div.search-results').find_elements_by_css_selector('li.search-result')
                _line = rows.find_elements_by_css_selector('li.search-result')[_i].find_element_by_css_selector('span.name.actor-name')
                # if member's name is 'LinkedIn Member', it can't be scraped.
                if 'LinkedIn Member' not in _line.text.strip():
                    _line.click()
                else:
                    continue

                try:
                    headline_row = WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.pv-top-card-section__body")))
                    try:
                        # If more button is in headline, click it.
                        headline_row.find_element_by_css_selector('button.pv-top-card-section__summary-toggle-button').click()
                    except:
                        pass

                    try:
                        full_name = headline_row.find_element_by_class_name('pv-top-card-section__name').text.strip()
                    except:
                        full_name = ''
                    try:
                        current_title = headline_row.find_element_by_class_name('pv-top-card-section__headline').text.strip()
                    except:
                        current_title = ''
                    try:
                        location = headline_row.find_element_by_class_name('pv-top-card-section__location').text.strip()
                    except:
                        location = ''

                    try:
                        company_desc = headline_row.find_element_by_class_name('pv-top-card-section__summary-text').text.strip()
                    except:
                        company_desc = ''

                except:
                    full_name = ''
                    current_title = ''
                    location = ''
                    company_desc = ''

                experience = []
                for i in range(10):
                    experience.append(['', '', '', ''])
                try:
                    #experience_row = self.driver.find_element_by_css_selector('section.pv-profile-section.experience-section')
                    experience_row = WebDriverWait(self.driver, 200).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "section.pv-profile-section.experience-section"))
                    )
                    try:
                        experience_row.find_element_by_css_selector('button.pv-profile-section__see-more-inline').click()
                    except:
                        pass

                    sub_experiences = WebDriverWait(experience_row, 200).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.pv-profile-section__section-info > li"))
                    )


                    for j, elm in enumerate(sub_experiences):
                        try:
                            job_title = elm.find_element_by_tag_name('h3').text.strip()
                        except:
                            job_title = ''

                        try:
                            company_name = elm.find_elements_by_tag_name('h4')[0].text.strip().split('\n')[1]
                        except:
                            company_name = ''

                        try:
                            period = elm.find_elements_by_tag_name('h4')[1].text.strip().split('\n')[1] + ': ' + elm.find_elements_by_tag_name('h4')[2].text.strip().split('\n')[1]
                        except:
                            period = ''

                        try:
                            geolocation = elm.find_elements_by_tag_name('h4')[3].text.strip().split('\n')[1]
                        except:
                            geolocation = ''

                        experience[j] = [job_title, company_name, period, geolocation]

                except:
                    pass

                education = []
                for i in range(5):
                    education.append(['', '', ''])

                try:
                    #education_row = self.driver.find_element_by_css_selector('section.pv-profile-section.education-section')
                    education_row = WebDriverWait(self.driver, 200).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "section.pv-profile-section.education-section"))
                    )

                    try:
                        education_row.find_element_by_css_selector(
                            'button.pv-profile-section__see-more-inline').click()
                    except:
                        pass

                    sub_educations = education_row.find_elements_by_css_selector(
                        'ul.pv-profile-section__section-info > li')

                    for j, elm in enumerate(sub_educations):
                        try:
                            edu_institution = elm.find_element_by_css_selector('div.pv-entity__degree-info > h3').text.strip()
                        except:
                            edu_institution = ''

                        try:
                            degree = elm.find_element_by_css_selector('div.pv-entity__degree-info').text.strip().replace(edu_institution, '').strip()
                            degree = ', '.join(degree.split('\n')[1:])
                        except:
                            degree = ''

                        try:
                            date = elm.find_element_by_css_selector('p.pv-entity__dates').text.strip().split('\n')[1]
                        except:
                            date = ''

                        education[j] = [edu_institution, degree, date]


                except:
                    pass

                self.output_data.append([
                    full_name, current_title, location, company_desc,
                    experience, education
                ])

                #print('OK')
                self.driver.execute_script("window.history.go(-1)")


        print('OK')

    def saveCSV(self):
        

if __name__ == '__main__':
    app = mainScraper('Duo Security')
    app.startScraping()