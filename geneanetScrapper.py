import os
import getpass
from seleniumbase import Driver
from geneanetItemToMd import GeneanetItemToMd

class GeneanetScrapper:
    def __init__(self, headless=True):
        self.path, filename = os.path.split(os.path.realpath(__file__))
        self.headless = headless
        self.driver = None
        self.is_connected = False
        self.total_page_nbr = 1
        self.current_page_nbr = 1

    def _start_browser(self):
        print("Start browser...")
        self.driver = Driver(browser="firefox",
                             uc=True, headless=False, locale_code='fr')

    def connect(self, id, password):
        self._start_browser()

        self.driver.get(
            "https://www.geneanet.org/connexion/")

        # Wait for the page to load
        css_id_field = '#_username'
        css_pwd_field = '#_password'
        css_connect_button = '#_submit'
        css_deny_cookie_button = '#tarteaucitronAllDenied2'
        self.driver.wait_for_element_visible(
            css_id_field, timeout=20)
        self.driver.wait_for_element_visible(
            css_deny_cookie_button, timeout=20)

        deny_cookie_button = self.driver.find_element(
            css_deny_cookie_button)
        # for a unknown reason we need to click multiples times
        # to makes the button accept the request
        deny_cookie_button.click()
        nbrIter = 0
        while (self.driver.is_element_visible(css_deny_cookie_button)):
            deny_cookie_button.click()
            nbrIter += 1
            if (nbrIter > 20):
                print(
                    "Unable to click on deny cookie button.\nUnable to connect to geneanet abort")
                return False

        # Enter the id
        id_field = self.driver.find_element(css_id_field)
        id_field.send_keys(id)

        # Enter the password
        pwd_field = self.driver.find_element(css_pwd_field)
        pwd_field.send_keys(password)

        # Click the connect button
        connect_button = self.driver.find_element(
            css_connect_button)
        connect_button.click()

        # Wait for the page to load
        css_family_name = 'div.row:nth-child(5) > div:nth-child(1) > input:nth-child(1)'
        self.driver.wait_for_element_visible(
            css_family_name, timeout=20)
        self.is_connected = True
        print("Has success to connect to Geneanet.net")
        return True

    def searchFamilyName(self, name):
        css_family_name = 'div.row:nth-child(5) > div:nth-child(1) > input:nth-child(1)'
        family_name_field = self.driver.find_element(css_family_name)
        family_name_field.send_keys(name)

        css_search_button = "button.button"
        search_button = self.driver.find_element(css_search_button)
        search_button.click()

        css_archive_toggle = "#categories_1-archives"
        self.driver.wait_for_element_visible(
            css_archive_toggle, timeout=20)
        self.loopOnPagesSearch()
        # archive_toggle = self.driver.find_element(css_archive_toggle)
        # archive_toggle.click()

        # css_civil_state = "div.checked:nth-child(1) > div:nth-child(2) > label:nth-child(1)"
        # self.driver.wait_for_element_visible(
        #     css_civil_state, timeout=20)

    def loopOnPagesSearch(self):
        totalPageNbr = self.getCurrentTotalPageNbr()
        #Add tqdm to this loop
        for i in range(totalPageNbr):
            self.clickOnNextPage()
            # if(i>3):
                # return
            #TODO look for each page


    # def getCurrentPageNbr(self):
    #     css_current_page = ".current > a:nth-child(1)"
    #     # current_page = self.driver.find_element(css_current_page)
    #     return int(self.driver.get_text(css_current_page))

    def getCurrentTotalPageNbr(self):
        # TODO it might not work with a low page number...
        # maybe reduce the number li:nth-child(7) until it found some thing
        css_total_page_nbr = ".pagination > li:nth-child(7) > a:nth-child(1)"
        self.total_page_nbr = int(self.driver.get_text(css_total_page_nbr))

    def clickOnNextPage(self):
        if(self.current_page_nbr == 1):
            css_click_on_next_page = f".pagination > li:nth-child(3) > a:nth-child(1)"
        elif(self.current_page_nbr == 2):
            css_click_on_next_page = f".pagination > li:nth-child(5) > a:nth-child(1)"
        elif(self.current_page_nbr == 3):
            css_click_on_next_page = f".pagination > li:nth-child(6) > a:nth-child(1)"
        elif(self.current_page_nbr == self.total_page_nbr -1)
            css_click_on_next_page = ".pagination > li:nth-child(8) > a:nth-child(1)"
        else:
            css_click_on_next_page = ".pagination > li:nth-child(7) > a:nth-child(1)"

        next_page_button = self.driver.find_element(css_click_on_next_page)
        next_page_button.click()
        self.current_page_nbr +=1

        css_archive_toggle = "#categories_1-archives"
        self.driver.wait_for_element_visible(
            css_archive_toggle, timeout=20)


    # def getRowInformations(self):
        # a.ligne-resultat:nth-child(1)
        # a.ligne-resultat:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(4) > em:nth-child(1)
        # a.ligne-resultat:nth-child(4)
        # a.ligne-resultat:nth-child(7)
        # a.ligne-resultat:nth-child(57)






