from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC



web = 'https://www.amazon.com'
driver_path = 'C:/Users/Pranav/Downloads/chromedriver_win32 (2)'

options = webdriver.ChromeOptions()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get(web)

driver.implicitly_wait(5)
keyword = "wireless charger"
search = driver.find_element(By.ID, 'twotabsearchtextbox')
search.send_keys(keyword)
# click search button
search_button = driver.find_element(By.ID, 'nav-search-submit-button')
search_button.click()

driver.implicitly_wait(5)

product_asin = []
product_name = []
product_price = []
product_ratings = []
product_ratings_num = []
product_link = []

items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
for item in items:
    # find name
    name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
    product_name.append(name.text)

    # find ASIN number 
    data_asin = item.get_attribute("data-asin")
    product_asin.append(data_asin)

    # find price
    whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
    fraction_price = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
    
    if whole_price != [] and fraction_price != []:
        price = '.'.join([whole_price[0].text, fraction_price[0].text])
    else:
        price = 0
    product_price.append(price)

    # find ratings box
    ratings_box = item.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')

    # find ratings and ratings_num
    if ratings_box != []:
        ratings = ratings_box[0].get_attribute('aria-label')
        ratings_num = ratings_box[1].get_attribute('aria-label')
    else:
        ratings, ratings_num = 0, 0
    
    product_ratings.append(ratings)
    product_ratings_num.append(str(ratings_num))
    
    # find link
    link = item.find_element(By.XPATH, './/a[@class="a-link-normal a-text-normal"]').get_attribute("href")
    product_link.append(link)
    
driver.quit()

# to check data scraped
print(product_name)
print(product_asin)
print(product_price)
print(product_ratings)
print(product_ratings_num)
print(product_link)