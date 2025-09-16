from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.headless = False
driver = webdriver.Firefox(options=options)
driver.get("https://www.audible.com/search")

# Get total number of pages
pagination = driver.find_element(By.XPATH, '//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME, "li")
last_page = int(pages[-2].text)
current_page = 1
driver.maximize_window()

# Data lists
book_title = []
book_author = []
book_date = []

while current_page <= last_page:
    time.sleep(2)

    # Wait until items are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "productListItem")]'))
    )

    items = driver.find_elements(By.XPATH, '//li[contains(@class, "productListItem")]')

    for item in items:
        try:
            title = item.find_element(By.XPATH, './/h3[contains(@class,"bc-heading")]').text
        except:
            title = ''
        try:
            author = item.find_element(By.XPATH, './/li[contains(@class,"authorLabel")]').text
        except:
            author = ''
        try:
            date = item.find_element(By.XPATH, './/li[contains(@class,"releaseDateLabel")]').text
        except:
            date = ''

        book_title.append(title)
        book_author.append(author)
        book_date.append(date)

    print(f"✅ Collected data from page {current_page}")

    # Go to the next page
    current_page += 1
    try:
        next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]/a')
        driver.execute_script("arguments[0].click();", next_page)
    except:
        print("🚫 No more pages available")
        break

driver.quit()

# Save to CSV
df_books = pd.DataFrame({
    'title': book_title,
    "author": book_author,
    'date': book_date
})
df_books.to_csv('book.csv', index=False)
print("💾 Data saved to book.csv")
