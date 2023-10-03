from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--window-size=1920,1080")
# options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])