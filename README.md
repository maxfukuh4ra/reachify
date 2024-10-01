# LinkedIn Profile Scraper and Email Automation

This project automates scraping LinkedIn profiles, generating personalized messages using OpenAI, and sending those messages via email. It leverages Selenium for web scraping, OpenAI for generating messages, and Gmail for sending personalized outreach emails.

## Features
- **LinkedIn Scraping**: Automatically logs into LinkedIn, scrapes profile information including name, headline, education, experience, and contact info (email).
- **Personalized Message Generation**: Uses OpenAI to create customized messages for each individual based on their LinkedIn profile data.
- **Email Automation**: Sends the personalized message to the scraped email addresses using Gmail.

## Prerequisites
- **Python 3.x**
- **Selenium** with Chrome WebDriver: automates web browser interaction.
- **OpenAI API Key**: generates personalized messages based on profile data.
- **Beautiful Soup4**: parses the HTML to extract data.
- **Gmail App Password**: allows logging into gmail account to send email

## Set-Up Instructions
**1.  Clone to repository**
```bash
git clone https://github.com/maxfukuh4ra/coldoutreach.git
cd linkedin-scraper
```

**2. Install required libraries**
```bash
pip install -r requirements.txt
```

**3. Edit the .env file with your credentials:**

**Create a LinkedIn App Password:**
1. Go to your Google Account settings.
2.  Navigate to Security and turn on 2-Step Verification.
3.  After that, you will be able to create App Passwords. Copy paste this into the .env.

**Create an OpenAI key:**
1. Create an OpenAI Account: visit [OpenAI's website](https://beta.openai.com/signup/) to sign up for an account.
1. After signing up, go to your [API Keys page](https://platform.openai.com/account/api-keys).
2. Click on **"Create new secret key"**.
3. Copy the generated API key. **Note:** You will only see this key once, so be sure to copy it immediately.

  
**4. Prepare the LinkedIn Profiles**: add LinkedIn profile URLs to a linkedin_profiles.csv file (one URL per line) in the project directory.


**5. Run the Script**:
```bash
python main.py
```
The terminal will prompt you to input your first & last name, LinkedIn username, and LinkedIn password. Follow the instruction and have fun! (sometimes, it may ask you to do a security question if has been done repeatedly so follow along on the Selenium Google Driver window and answer accordingly!)
