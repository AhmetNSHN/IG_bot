import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

TIME_OUT = 15

class unfollowerslist_maker:
    def __init__(self):
        self.USERNAME = ''  # -> your username here
        self.PASSWORD = ''  # -> your password here
        self.scraped_user = ''  # -> username that will be checked here

        # selenium configurations ------------------------------------------------
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        self.bot = webdriver.Chrome(desired_capabilities=caps)
        options = webdriver.ChromeOptions()
        mobile_emulation = {
            "userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19'
                         ' (KHTML, like Gecko) Chrome/83.0.1025.133 Mobile Safari/535.19'
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.bot.get("https://instagram.com/")
        self.bot.set_window_size(1500, 1000)

        self.login()

        self.followers = []
        turn = "//a[contains(@href, '/followers')]"
        self.scrape(turn, self.followers)

        self.bot.find_element(By.CSS_SELECTOR, '.x1qjc9v5.x9f619.x78zum5.xdt5ytf.x1iyjqo2.xl56j7k').click()
        time.sleep(2)

        self.followed = []
        turn = "//a[contains(@href, '/following')]"
        self.scrape(turn, self.followed)

        self.unfollow_list = []
        self.not_following()

    def login(self):

        print("Logging in...")
        # USERNAME
        username_field = WebDriverWait(self.bot, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
        username_field.send_keys(self.USERNAME)
        # PASSWORD
        password_field = WebDriverWait(self.bot, TIME_OUT).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
        password_field.send_keys(self.PASSWORD)
        # LOGIN
        WebDriverWait(self.bot, TIME_OUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div'))).click()

    def scrape(self, turn, list): #scrapes usernames from followers and following popups

        time.sleep(5)
        link = 'https://www.instagram.com/{}/'.format(self.scraped_user)
        self.bot.get(link)
        WebDriverWait(self.bot, TIME_OUT).until(EC.presence_of_element_located((By.XPATH, turn))).click()
        print('button clicked')
        time.sleep(3)
        print('Scrapping...')

        ActionChains(self.bot).send_keys(Keys.END).perform()
        time.sleep(3)

        self.scroller()
        followers = self.bot.find_elements(By.CSS_SELECTOR, ".x9f619.xjbqb8w.x1rg5ohu.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1")

        i = 0
        for f in followers:
            # print(f.text)
            list.append(f.text)
            i = i + 1
        print(f"scraped users in first part: {i} . Be sure that number of user match with instagram statistics otherwise check your internet connection")


    def scroller(self): # scrolls followers and following popups
        command = """
            page = document.querySelector("._aano");
            page.scrollTo(0, page.scrollHeight);
            var page_end = page.scrollHeight;
            return page_end;
            """
        page_end = self.bot.execute_script(command)
        while True:
            end = page_end
            time.sleep(2)
            page_end = self.bot.execute_script(command)
            # print("scraping>>>")
            if end == page_end:
                break

    def not_following(self):
        for f in self.followed:
            if f not in self.followers:
                print(f)
                self.unfollow_list.append(f)


run = unfollowerslist_maker()
# @ahmetncsahin
