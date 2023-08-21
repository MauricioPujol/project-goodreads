from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
 
# instantiate options 
options = webdriver.ChromeOptions() 
 
# run browser in headless mode 
options.headless = True 
 
# instantiate driver 
driver = webdriver.Chrome(service=ChromeService( 
	ChromeDriverManager().install()), options=options) 
 
# load website 
url = 'https://www.goodreads.com/book/show/141263.Ars_ne_Lupin_versus_Herlock_Sholmes' 
 
# get the entire website content 
driver.get(url) 

# select elements by class name 
elements = driver.find_elements(By.CLASS_NAME, 'text-container') 
for title in elements: 
	# select H2s, within element, by tag name 
	heading = title.find_element(By.TAG_NAME, 'h2').text 
	# print H2s 
	print(heading)