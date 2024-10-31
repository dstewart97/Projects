#### Review Scrapper Packages ####
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import random
import time



"""

The below program uses webdriving through selenium to extract reviews, or other type of short-form text data (i.e., social media post). This code is specific for Credit Karma, but this can be 
used a template for any other site.

"""

class ReviewScrapper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = self._initialize_driver()
        self.data = pd.DataFrame(columns = ["Date", "Product", "Credit_Type", "Rating", "Title", "CK_Member", "Verified_Customer", "Body", "Helpful", "Not_Helpful", "Comment"])


    def _initialize_driver(self):
        service = Service(self.driver_path)
        return webdriver.Edge(service = service)
    

    def scrape_reviews(self, product_dict):
        for credit_type, product_list in product_dict.items():
            for product in product_list:
                self.scrape_product_reviews(product, credit_type)


    def scrape_product_reviews(self, product, credit_type):
        page = 1
        #Page < x when pulling less than all reviews
        while True: 
            try:
                # Open page based on parameters input
                url = f'https://www.creditkarma.com/reviews/credit-card/single/id/{product}?pg={page}'
                self.driver.get(url)
                print(f"Extracting data for {product} on Page {page} under category: {credit_type}")

                # Implement extraction logic here...
                # Check if there are reviews on this page
                try:
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="top-of-reviews"]/div[3]/div[1]/article')))
                except:
                    print(f"No more reviews found for {product} on page {page}, review {i}. Moving to the next product.")
                    break

                # Loop through the divs on the current page -- break if no more reviews
                for i in range(1, 11):
                    try:
                        main_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="top-of-reviews"]/div[3]/div[{i}]/article')))
                    except Exception as e:
                        print(f"No more reviews for {product} on page {page}...")
                        break  
                    if main_element is None:
                        break

                    # Initialize a dictionary to hold extracted data
                    div_data = {"Product": product, "Credit_Type": credit_type}

                    # Extract unique elements by tag
                    tags = ['span', 'div', 'h5']
                    unique_elements = {tag: [] for tag in tags}
                    for tag in tags:
                        elements = main_element.find_elements(By.TAG_NAME, tag)
                        for element in elements:
                            text = element.text
                            if text and text not in unique_elements[tag]:
                                unique_elements[tag].append(text)

                    # Populate review data from unique elements
                    div_data["Verified_Customer"] = unique_elements['span'][1] if len(unique_elements['span']) > 1 else "Not Verified"
                    div_data["Date"] = unique_elements['span'][0] if unique_elements['span'] else "No Date"
                    div_data["CK_Member"] = unique_elements['div'][1] if len(unique_elements['div']) > 2 else "Unknown"

                    # Handle 'More' cases for Helpful, Not Helpful, and Comment counts
                    has_more = False
                    for j, div_text in enumerate(unique_elements['div']):
                        if "More" in div_text:
                            has_more = True
                            # Assign counts from the next element after 'More'
                            div_data["Helpful"] = unique_elements['div'][-3] 
                            div_data["Not_Helpful"] = unique_elements['div'][-2] 
                            div_data["Comment"] = unique_elements['div'][-1]
                            break
                    # If no 'More' was found, extract counts from default position 
                    if not has_more and len(unique_elements['div']) > 3:
                        counts = unique_elements['div'][3].split('\n')
                        div_data["Helpful"] = counts[0] if counts else "0"
                        div_data["Not_Helpful"] = counts[1] if len(counts) > 1 else "0"
                        div_data["Comment"] = counts[2] if len(counts) > 1 else "0"

                    # Extract comment body
                    try:
                        div_data['Body'] = main_element.find_element(By.TAG_NAME, 'p').text
                    except:
                        div_data["Body"] = "No Comment"
                    
                    # Extract review title
                    div_data["Title"] = unique_elements['h5'][0] if unique_elements['h5'] else "No Title"

                    # Extract ratings from aria-labels
                    divs = main_element.find_elements(By.TAG_NAME, 'div')
                    for div in divs:
                        aria_label = div.get_attribute("aria-label")
                        if aria_label: 
                            div_data["Rating"] = aria_label
                            break

                    # Append the div_data to all_data DataFrame
                    self.data = pd.concat([self.data, pd.DataFrame(div_data, index=[0])], ignore_index=True)

                page += 1
                time.sleep(random.uniform(1, 10))

            except Exception as e:
                print(f"Error extracting Product: {product} on Page: {page}; Erro: {e}")
                break

    def close_driver(self):
        self.driver.quit()


