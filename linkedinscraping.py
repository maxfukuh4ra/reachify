import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

def setup_driver(driver_path):
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    return driver

def login_linkedin(driver, username_str, password_str):
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    username = driver.find_element(By.ID, 'username')
    username.send_keys(username_str)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(password_str)
    password.send_keys(Keys.RETURN)
    time.sleep(3)

def scrape_profile(url, driver):
    driver.get(url)
    time.sleep(3)

    # parse with bs4
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # exclude other parts such as side-bar
    profile_main_content = soup.find('main', class_='scaffold-layout__main')
    if not profile_main_content:
        return None

    profile_data = {}
    name_tag = profile_main_content.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words')
    profile_data['name'] = name_tag.get_text(strip=True) if name_tag else "N/A"

    headline_tag = profile_main_content.find('div', class_='text-body-medium break-words')
    profile_data['headline'] = headline_tag.get_text(strip=True) if headline_tag else "N/A"

    education_div = profile_main_content.find('div', id='education')
    education_details = {} # dictionary to hold education information
    if education_div:
        education_entries = education_div.find_next('ul')
        if education_entries:
            for entry in education_entries.find_all('li', class_='artdeco-list__item'):
                school_name_tag = entry.find('span', {'aria-hidden': 'true'})
                school_name = school_name_tag.get_text(strip=True) if school_name_tag else "N/A"

                degree_info_tag = entry.find('span', class_='t-14 t-normal')
                degree_info = degree_info_tag.find('span', {'aria-hidden': 'true'}).get_text(strip=True) if degree_info_tag else "N/A"

                date_range_tag = entry.find('span', class_='t-14 t-normal t-black--light')
                date_range = date_range_tag.find('span', {'aria-hidden': 'true'}).get_text(strip=True) if date_range_tag else "N/A"

                education_details[school_name] = {
                    "Degree": degree_info,
                    "Dates": date_range
                }
    profile_data['education_details'] = education_details

    experience_div = profile_main_content.find('div', id='experience')
    experience_details = {} # dictionary to store experience details
    if experience_div:
        experience_entries = experience_div.find_next('ul')
        if experience_entries:
            for entry in experience_entries.find_all('li', class_='artdeco-list__item'):
                position_name_tag = entry.find('span', {'aria-hidden': 'true'})
                position_name = position_name_tag.get_text(strip=True) if position_name_tag else "N/A"

                company_name_tag = entry.find('span', class_='t-14 t-normal')
                company_name = company_name_tag.find('span', {'aria-hidden': 'true'}).get_text(strip=True) if company_name_tag else "N/A"

                date_range_tag = entry.find('span', class_='t-14 t-normal t-black--light')
                date_range = date_range_tag.find('span', {'aria-hidden': 'true'}).get_text(strip=True) if date_range_tag else "N/A"

                experience_details[company_name] = {
                    "Position": position_name,
                    "Dates": date_range
                }
    profile_data['experience_details'] = experience_details


    # email section requires the open the contact card first
    contact_info_url = f"{url}/overlay/contact-info/"
    driver.get(contact_info_url)
    time.sleep(3)

    # re-parse
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    email_section = soup.find('h3', class_='pv-contact-info__header t-16 t-black t-bold')
    if email_section:
        email_tag = email_section.find_next('a', href=lambda x: x and x.startswith('mailto:'))
        if email_tag:
            email_text = email_tag.get_text(strip=True)
            profile_data['email'] = email_text

    return profile_data
