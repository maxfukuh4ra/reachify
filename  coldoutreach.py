import pandas as pd 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv() 

# Step 3: setting up openAI prompt
from openai import OpenAI
api_keys = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_keys)

def generate_personalized_message(name, headline, education_details, experience_details, about_text):
    prompt = f"""
    Write a personalized outreach message for a person named {name}. Their LinkedIn headline is: "{headline}".
    Education details: "{education_details}". Experience details: "{experience_details}". 
    About section: "{about_text}". Focus on the skills they have, and make it sound friendly and inviting. 
    Make sure it begins with 
    Dear {name}, 
    """
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message)

    return completion.choices[0].message





# Step 1: leads arrive on a sheet with links to their LinkedIn profiles.
df = pd.read_csv('linkedin_profiles.csv', header=None)
urls = df[0]


# Step 2: scrape information from the profiles.
driver_path = './chromedriver-mac-arm64/chromedriver'  # path to your ChromeDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# LinkedIn login credentials
username_str = os.getenv("LINKEDIN_USERNAME")
password_str = os.getenv("LINKEDIN_PASSWORD")
driver.get('https://www.linkedin.com/login')
time.sleep(2)  # let page load
# find and fill username
username = driver.find_element(By.ID, 'username')
username.send_keys(username_str)
# find and fill password
password = driver.find_element(By.ID, 'password')
password.send_keys(password_str)
# submit log in form
password.send_keys(Keys.RETURN)  # return button to submit the form
time.sleep(10)

for url in urls:
    driver.get(url)
    time.sleep(3)

    # parse with bs4
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # exclude other parts such as side-bar
    profile_main_content = soup.find('main', class_='scaffold-layout__main')
    if profile_main_content:
        name_tag = soup.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words')
        name = name_tag.get_text(strip=True) if name_tag else "N/A"

        headline_tag = soup.find('div', class_='text-body-medium break-words')
        headline = headline_tag.get_text(strip=True) if headline_tag else "N/A"

        about_div = profile_main_content.find('div', id='about')
        if about_div:
            about_text_tag1 = about_div.find_next('div', class_='display-flex ph5 pv3')
            if about_text_tag1:
                about_text_tag2 = about_text_tag1.find('span', {'aria-hidden': 'true'})
                if about_text_tag2:
                    about_text = about_text_tag2.get_text(strip=True)
        else:
            about_text = 'N/A'
            

        education_div = profile_main_content.find('div', id='education')
        education_details = {}  # dictionary to hold education information
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
        education_text = "\n".join([f'{school}: {details["Degree"]}, {details["Dates"]}' for school, details in education_details.items()])


        experience_div = profile_main_content.find('div', id='experience')
        experience_details = {}  # dictionary to store experience details
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
        experience_text = "\n".join([f'{company}: {details["Position"]}, {details["Dates"]}' for company, details in experience_details.items()])
        print(experience_text)

        # called the OpenAI integrating function
        personalized_message = generate_personalized_message(name, headline, education_text, experience_text, about_text)

        # print the generated message
        print(f'Personalized Message for {name}:\n{personalized_message}\n')

# Close the browser after scraping
driver.quit()
