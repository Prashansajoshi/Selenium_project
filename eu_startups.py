from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

gecko_driver_path =r"c:\Users\Dell\Downloads\geckodriver-v0.34.0-win64\geckodriver.exe"

firefox_options = Options()
firefox_options.binary_location = r"c:\Program Files (x86)\Mozilla Firefox\firefox.exe"
driver = webdriver.Firefox(options=firefox_options)
driver.get("https://www.eu-startups.com/directory/")

# Wait for the element with ID "main" to be present
try:

    # Create an empty list to store the scraped data
    data_list = []

     # Function to scrape titles and categories on the current page
    def scrape_titles_with_category():
        listings = driver.find_elements(By.CLASS_NAME, 'wpbdp-listings-list')
        for listing in listings:

            titles = listing.find_elements(By.CSS_SELECTOR, 'h3 a')
            
            
            for title in titles:
                href = title.get_attribute('href')
            

                new_tab_script = f'window.open("{href}", "_blank");'
                driver.execute_script(new_tab_script)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(5)
                company_name = driver.find_element(By.CSS_SELECTOR,'div.td-page-header').text
                category = driver.find_element(By.XPATH, '//div[contains(@class, "wpbdp-field-category")]//div[@class="value"]/a').text
                tags = driver.find_element(By.XPATH,'//div[contains(@class, "wpbdp-field-tags")]//div[@class="value"]').text
                founded = driver.find_element(By.XPATH,'//div[contains(@class, "wpbdp-field-founded")]//div[@class="value"]').text
                based_on = driver.find_element(By.XPATH,'//div[contains(@class, "wpbdp-field-based_in")]//div[@class="value"]').text
                total_Funding = driver.find_element(By.XPATH,'//div[contains(@class, "wpbdp-field-total_funding")]//div[@class="value"]').text
                website = driver.find_element(By.XPATH,'//div[contains(@class, "wpbdp-field-website")]//div[@class="value"]').text
                Company_Status = driver.find_element(By.XPATH,'//div[contains(@class, "wpbdp-field-company_status")]//div[@class="value"]').text

                 # Append the scraped data to the data_list'

                data_list.append({
                    "Company Name": company_name,
                    "Category": category,
                    "Tags": tags,
                    "Founded": founded,
                    "Based On": based_on,
                    "Total Funding": total_Funding,
                    "Website": website,
                    "Company Status": Company_Status
                })

                time.sleep(10)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    # Main loop for pagination
    while True:
        # Scraping titles on the current page
        scrape_titles_with_category()

        # Checking if there's a 'Next' button for pagination
        next_button = driver.find_element(By.XPATH, '//*[@id="wpbdp-listings-list"]/div[12]/span[2]')
        if 'disabled' in next_button.get_attribute('class'):
            # If 'Next' button is disabled, break out of the loop
            break

        # Clicking on 'Next' button to navigate to the next page
        next_button.click()

        # Waiting for the next page to load
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))


finally:
    driver.quit()

     # Write the scraped data to a JSON file
    with open('scraped_data.json', 'w') as f:
        json.dump(data_list, f, indent=4)