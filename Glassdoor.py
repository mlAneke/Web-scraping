import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json

main_url = "https://www.glassdoor.com"
url = "https://www.glassdoor.com/Job/"

#to enter the keywords into search field
driver = webdriver.Chrome()
driver.get(url)
search_field = driver.find_element(By.XPATH, "//*[@id='sc.keyword']")
location_field = driver.find_element(By.XPATH, "//*[@id='sc.location']")
text_search = "Test Automation Engineer"
text_location = "Espoo"
search_field.send_keys(text_search)
location_field.send_keys(text_location)
submit_button = driver.find_element(By.XPATH, "//*[@id='scBar']/div/button")
submit_button.click()
time.sleep(3)
# Get the page source after submitting the search form
page_source = driver.page_source

# Create a BeautifulSoup object from the page source
soup = BeautifulSoup(page_source, 'html.parser')

#to extract job titles
job_listings = soup.find_all("div", class_="job-search-3x5mv1")
#job_titles = [title.get_text() for title in job_titles]

# Create a list to store the job data
jobs = []

for listing in job_listings:
    # Extract the title, link, company, and location
    title = listing.find("div", class_="job-title mt-xsm").get_text().strip()
    job_url = listing.find("a")["href"]
    link = main_url + job_url
    company = listing.find("div", class_="job-search-8wag7x").get_text().strip()
    location = listing.find("div", class_="location mt-xxsm").get_text().strip()

    if "Espoo" in location:
    # Create a dictionary for the job data
        job_data = {
            "title": title,
            "link": link,
            "company": company,
            "location": location
        }

        # Add the job data to the list
        jobs.append(job_data)

# Save the job data as JSON
with open("job_glassdoor_data.json", "w") as outfile:
    json.dump(jobs, outfile, indent=4)