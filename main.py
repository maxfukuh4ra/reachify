import pandas as pd
from linkedinscraping import setup_driver, login_linkedin, scrape_profile
from message_generator import generate_personalized_message
import getpass

# set up selenium driver
driver_path = './chromedriver-mac-arm64/chromedriver'
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
        print(f'Personalized Message for {profile_data["name"]}:\n{personalized_message}\n')

# Close the browser after scraping
driver.quit()
