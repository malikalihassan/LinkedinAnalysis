import textwrap
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import *
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import pickle
import os
import time
from utils import *
import re
import json
from openai import OpenAI
import csv

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--start-maximized")









 # Update the path to your chrome driver
driver = webdriver.Chrome( options=chrome_options)

# LinkedIn login URL
login_url = "https://www.linkedin.com/login"
Profile_url = ""
Email = "testingmovig@gmail.com"
password = "Movig@123"
GPT_API_KEY = None

# Load LinkedIn and login
def linkedin_login():
    driver.get(login_url)
    time.sleep(10)
    display = Display(visible=0, size=(800, 600))
    display.start()
   
    try:
        driver.find_element(By.ID, "username").send_keys(Email)
    except:
        print("username is already there")
    driver.find_element(By.ID, "password").send_keys(password)
    
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # Wait for login to complete. Extra time on first login in order to perform 2f.
    time.sleep(300)
    
   
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def load_cookies():
    try:
        if os.path.exists("cookies.pkl"):
            cookies = pickle.load(open("cookies.pkl", "rb"))
            driver.get("https://www.linkedin.com")
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()

            # Check if login is successful after using cookies
            time.sleep(5)  # Wait for the page to load
            if "feed" in driver.current_url:
                print("Logged in using cookies")
                return True
            else:
                print("Failed to login using cookies")
                return False
        else:
            return False
    except:
        return False


def text_or_default(element, selector, default=None):
    """Same as one_or_default, except it returns stripped text contents of the found element
    """
    try:
        return element.select_one(selector).get_text().strip()
    except Exception as e:
        return default


def exp(soup):
    experiences = dict.fromkeys(
            ['jobs', 'education', 'volunteering'], [])
    try:
        container = one_or_default(soup, '.background-section')

        jobs = all_or_default(
            container, '#experience-section ul .pv-position-entity')
        jobs = list(map(get_job_info, jobs))
        jobs = flatten_list(jobs)

        experiences['jobs'] = jobs

        schools = all_or_default(
            container, '#education-section .pv-education-entity')
        schools = list(map(get_school_info, schools))
        experiences['education'] = schools

        volunteering = all_or_default(
            container, '.pv-profile-section.volunteering-section .pv-volunteering-entity')
        volunteering = list(map(get_volunteer_info, volunteering))
        experiences['volunteering'] = volunteering
    except Exception as e:
       print(
            "Failed while determining experiences. Results may be missing/incorrect: %s", e)
    finally:
        return experiences

def extract_about_section(soup: BeautifulSoup) -> str:

    about_section = soup.find('section', class_='artdeco-card pv-profile-card break-words mt2')
    
    if about_section:
        # Find all the text within the section
        text = about_section.get_text(separator=" ", strip=True)
        return text
    else:
        return "No about section found."

def extract_skills(soup: BeautifulSoup) -> list:
    # Find all sections
    sections = soup.find_all('section', class_='artdeco-card pv-profile-card break-words mt2')
 
    for section in sections:
        
        # Look for the section with the 'Services' heading
        heading = section.find('h2', class_='pvs-header__title')
        if heading and 'Services' in heading.get_text(strip=True):
            # Extract skills within strong tags
            skills = section.find_all('strong')
            skills_list = [skill.get_text(strip=True) for skill in skills]
    return skills_list
    
    

    
        



def get_profile_link():
    
    time.sleep(5)
    
   
    try:
        profile_link = driver.find_element(By.XPATH, "//a[contains(@class, 'ember-view') and contains(@class, 'block') and contains(@href, '/in/')]")
        return profile_link.get_attribute('href')
        # return profile_link
    except Exception as e:
        print("Error fetching profile link:", e)
        return None

def scrape_profile(profile_url):
    driver.get(profile_url)

    time.sleep(5)  # Wait for the profile to load
    name=""
    about=""
    headline=""
    services=""
    about_section=""
    try:
        # Scrape Name
        try:
            name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").text
        except:
            print("Error in name")

        try:
            headline = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium.break-words").text
        except:
            print("Error in headline")
        profile_html=driver.page_source
        soup=BeautifulSoup(profile_html,'html.parser')
        
        
        try:
            about_section= extract_about_section(soup)
        except:
            print("Error in headline")
        try:
            
            services= extract_skills(soup)
        
        except:
            print("Error in Services")

        print(f"Name: {name}")
        print(f"Headline: {headline}")
        print(f"About: {about_section}")
        print(f"Skills: {services}")
   
        return name,headline,services,about_section
   

    except Exception as e:
        print(f"Error scraping profile: {e}")
        return name,headline,services,about_section
        









def analyze_analyze_data(data):
    
    client = OpenAI(
   
    api_key= GPT_API_KEY,
    )
    
    
    messages = [
            {
                "role": "system",
                "content": textwrap.dedent("""
    You are an expert LinkedIn profile consultant. Given the following information:

    

    Provide the following:

    1. **Profile Completeness**: Analyze if the profile is fully optimized and give suggestions for improving visibility (headline, summary, skills, experience, etc.).
    2. **SEO for LinkedIn**: Suggest how the user can optimize their profile for search results, including keyword improvements based on their industry and desired job role.
    3. **Content Suggestions**: Give suggestions for articles or posts the user can write that align with their expertise and target audience.
    """)
            },
            {
                "role": "user",
                "content": data
            },
        ]

    response = client.chat.completions.create(
        model= "gpt-3.5-turbo",
        messages=messages,
        temperature= 0.7,
        max_tokens=800,
        functions=[
            {
                "name": "save_analysis",
                "description": "This function analyzes the about section and gives suggession to linkedin users",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "profile_completeness": {
                            "type": "string",
                            "description": "Analyze if the profile is fully optimized and give suggestions for improving visibility. Consider experience and skills are already added"
                            },
                        "linkedin_seo":{
                            "type": "string",
                            "description":  "Suggest how the user can optimize their profile for search results, including keyword improvements based on their industry and desired job role."
                            
                        },
                        "content_suggestion": {
                            "type": "string",
                            "description": "Give suggestions for articles or posts the user can write that align with their expertise and target audience."
                        },
                      
                        
                    },
                    "required": ["profile_completeness","linkedin_seo","content_suggestion"]
                }
            }
        ],
        function_call={
            "name": "save_analysis"
        }
    )
    
    arguments = response.choices[0].message.function_call.arguments
    print(arguments)
    return arguments

def write_results_to_csv(final_results, file_path='results.csv'):
    # Define the column names
    fieldnames = ["profile", "name", "headline", "about_section", "services",'linkedin_seo', 'profile_completion', 'content_suggestion']
    
    # Open the CSV file for writing
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the column names
        writer.writeheader()
        
        # Write each result as a row in the CSV
        for result in final_results:
            writer.writerow(result)
    
    print(f"Data has been written to {file_path}")



def main():
    # Check if GPT API key is provided
    if GPT_API_KEY is None:
        return "Please enter your GPT API key"
    
    final_results = []
    
    try:
        # Load cookies, or login with credentials if cookies not found
        if not load_cookies():
            linkedin_login()
        
        # List of LinkedIn profiles to scrape
        Profiles = [
            'https://www.linkedin.com/in/muhammad-usman-nasir-64228b87/',
            'https://www.linkedin.com/in/suhail-abbas-498342259/',
            'https://www.linkedin.com/in/tatev-gevorgyanrecruiter/',
            'https://www.linkedin.com/in/nabeel129/'
        ]
        
        # Loop through each profile
        for profile in Profiles:
            try:
                # Scrape profile data
                name, headline, services, about_section = scrape_profile(profile)
            except Exception as e:
                print(f"Error scraping profile {profile}: {e}")
                continue  # Skip this profile if scraping fails

            # Prepare data for GPT analysis
            data = f"""
            Name: {name}
            Headline: {headline}
            Services: {services}
            About Section: {about_section}
            """
            
            try:
                # Analyze data with GPT API
                a_data = analyze_analyze_data(data)
                a_data = json.loads(a_data)
            except Exception as e:
                print(f"Error analyzing profile {profile}: {e}")
                continue  # Skip if analysis fails

            # Compile result dictionary
            result = {
                "profile": profile,
                "name": name,
                "headline": headline,
                "about_section": about_section,
                "services": services,
                "profile_completion": a_data.get('profile_completeness', 'N/A'),
                "linkedin_seo": a_data.get('linkedin_seo', 'N/A'),
                "content_suggestion": a_data.get('content_suggestion', 'N/A')
            }
            
            # Append result to final results list
            final_results.append(result)
        
        # Write final results to CSV
        write_results_to_csv(final_results, file_path='results.csv')

    finally:
        # Quit the driver at the end
        driver.quit()

# Call main function when the script is executed
if __name__ == "__main__":
    result = main()
    print(result)
