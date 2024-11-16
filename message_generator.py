from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = openai_api_key)

def generate_personalized_message(profile_data, your_name):
    name = profile_data['name']
    headline = profile_data['headline']
    education_details = "\n".join([f'{school}: {details["Degree"]}, {details["Dates"]}' for school, details in profile_data['education_details'].items()])
    experience_details = "\n".join([f'{company}: {details["Position"]}, {details["Dates"]}' for company, details in profile_data['experience_details'].items()])

    prompt = f"""
    Write a personalized outreach message for a person named {name}. Below is the following information.
    LinkedIn Headline: "{headline}".
    Education Details: "{education_details}".
    Experience Details: "{experience_details}". 
    
    Focus on their experience details the most. The main goal is to connect with them to learn more about what they do. 
    Ask them if they have any availability in the next week or so to connect via online such as Zoom.

    Finally, make sure it begins with:
    Dear {name}, 

    and ends with:
    Best,
    {your_name}
    """
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content
