import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class unfolllowlist_maker:
    def __init__(self):
        self.USERNAME = '' #-> your username here
        self.PASSWORD = '' #-> your password here
        usr = "" #-> username that will be checked here
        self.bot = webdriver.Safari()

        self.login()

        self.followers = []
        turn = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span'
        self.scrape(usr, turn, self.followers)

        # self.bot.find_element_by_xpath(
        #     '/html/body/div[4]/div/div/div[1]/div/div[2]/button').click()

        self.followed = []
        turn = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span'
        self.scrape(usr, turn, self.followed)
        self.unfollow_list = []
        self.not_following()


    def login(self):
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")

        mobile_emulation = {
            "userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/83.0.1025.133 Mobile Safari/535.19'
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        self.bot.get("https://instagram.com/")
        self.bot.set_window_size(1500, 1000)
        time.sleep(5)
        self.bot.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]').click()
        print("Logging in...")
        time.sleep(1)
        username_field = self.bot.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[1]/div/label/input')
        username_field.send_keys(self.USERNAME)

        find_pass_field = (
            By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        WebDriverWait(self.bot, 100).until(
            EC.presence_of_element_located(find_pass_field))
        pass_field = self.bot.find_element(*find_pass_field)
        WebDriverWait(self.bot, 1).until(
            EC.element_to_be_clickable(find_pass_field))
        pass_field.send_keys("0")
        # bot.find_element_by_xpath(
        #     '///*[@id="loginForm"]/div/div[3]n').click()
        time.sleep(2)

        find_pass_field = (
            By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        WebDriverWait(self.bot, 100).until(
            EC.presence_of_element_located(find_pass_field))
        pass_field = self.bot.find_element(*find_pass_field)
        WebDriverWait(self.bot, 1).until(
            EC.element_to_be_clickable(find_pass_field))
        pass_field.send_keys(self.PASSWORD)
        self.bot.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(5)

    def scrape(self, username, turn, list):

        link = 'https://www.instagram.com/{}/'.format(username)
        self.bot.get(link)
        time.sleep(5)
        print('button will be clicked...')
        self.bot.find_element_by_xpath(turn).click()# button
        print('button clicked')
        time.sleep(5)
        print('Scrapping...')

        ActionChains(self.bot).send_keys(Keys.END).perform()
        time.sleep(3)

        flv = self.bot.find_elements_by_xpath(
            '//*[@id="react-root"]/section/main/div/ul/div/li/div/div[1]/div[2]/div[1]/a')
        self.scroller()
        followers = self.bot.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")

        i = 0
        for f in followers:
            # print(f.text)
            list.append(f.text)
            i = i + 1
        print(f"scraped users in first part: {i} . Be sure that number of user match with instagram statistics otherwise check your internet connection")

    def scroller(self):
        command = """
            page = document.querySelector(".isgrP");
            page.scrollTo(0, page.scrollHeight);
            var page_end = page.scrollHeight;
            return page_end;
            """
        page_end = self.bot.execute_script(command)
        while True:
            end = page_end
            time.sleep(1)
            page_end = self.bot.execute_script(command)
            print("scraping>>>")
            if end == page_end:
                break


    def not_following(self):
        for f in self.followed:
            if f not in self.followers:
                print(f)
                self.unfollow_list.append(f)


run = unfolllowlist_maker()

#@ahmetncsahin

