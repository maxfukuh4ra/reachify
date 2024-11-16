import pandas as pd
from linkedinscraping import setup_driver, login_linkedin, scrape_profile
from message_generator import generate_personalized_message
import getpass
from send_email import send_email

# set up selenium driver
driver_path = './chromedriver'
driver = setup_driver(driver_path)

# log into linkedin
# change to input prompted
your_name = input("Enter your first and last name: ")
username_str = input("Enter your LinkedIn username: ")
password_str = getpass.getpass("Enter your LinkedIn password: ")
login_linkedin(driver, username_str, password_str)


# read URLs from data
df = pd.read_csv('linkedin_profiles.csv', header=None)
urls = df[0]

# loop through
for url in urls:
    # scrap each profile
    profile_data = scrape_profile(url, driver)
    if profile_data:
        # generate personalized message 
        personalized_message = generate_personalized_message(profile_data, your_name)
        print(profile_data['email'])
        send_email(profile_data['email'], 'Request to Connect', personalized_message)


driver.quit()
