from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from ultra import checkdist
import time
import os

# Set chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver_service = Service('/usr/bin/chromedriver')
page = webdriver.Chrome(service=driver_service, options=chrome_options)
# Flask app's URL
page.get('http://localhost:5000')  
w
actions = ActionChains(page)

while True:
    distance = checkdist()
    if distance < 10:  # If distance is less than 10 cm
        actions.key_up('w')  # Release 'w' key
        actions.perform()
        break  # End the script
    else:
        actions.key_down('w')  # Hold 'w' key
        actions.perform()
    time.sleep(1)  # Wait for 1 second

page.quit()