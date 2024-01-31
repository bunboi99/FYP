# interaction with web server

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import ultra

# Create a new instance of the Chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/home/wangding/Downloads/chromedriver-linux64/chromedriver', options=options)

# Go to the webpage that you want to access
driver.get("http://192.168.1.98:5000")

# Wait for the page to load
time.sleep(5)

while True:
    # Call checkdist() and multiply the result by 100
    distance = ultra.checkdist() * 100
    print("%.2f cm" % distance)
    time.sleep(1)

    # While the distance is greater than 10cm, press 'w' on the webpage
    while ultra.checkdist() * 100 > 10:
        body = driver.find_element_by_tag_name('body')
        body.send_keys('w')
        time.sleep(0.1)  # Wait a bit between each key press