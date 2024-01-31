from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# add any options you need
# for example: options.add_argument("--headless")

driver = webdriver.Chrome('/usr/bin/chromedriver')
driver.get("https://www.google.com")