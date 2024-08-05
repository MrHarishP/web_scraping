import requests
from bs4 import BeautifulSoup
import pandas as pd

def getValueFromSpan(li):
    span_tag = li.find('span')
    print(li)
    if span_tag:
        return span_tag.get_text(strip=True)
    
        

# Function to extract company data from the given URL
def extract_company_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the company name from the h2 tag inside 'course-details-banner-content' class
        company_name = soup.select_one('div.course-details-banner-content h2').get_text(strip=True)
        
        # Extract mobile number and WhatsApp number from the 'sidebar-description' class
        sidebar = soup.select_one('div.sidebar-description')
        print(sidebar)
        if sidebar:
            mobile_number = None
            whatsapp_number = None
            
            # Assuming that mobile and WhatsApp numbers are contained in <p> tags or similar
            lists = sidebar.find_all('li')
            for li in lists:
                text = li.get_text(strip=True) 
                if 'Mob No' in text:
                    mobile_number=getValueFromSpan(li)            
                elif ('Whatsapp No' in text):
                    whatsapp_number=getValueFromSpan(li)            
            
            return {
                'company_name': company_name,
                'mobile_number': mobile_number,
                'whatsapp_number': whatsapp_number
            }
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# URL to extract data from
url = 'https://ed.indexpo.co.in/expo-detail/269'
company_data = extract_company_data(url)

# Save the data to a CSV file
if company_data:
    df = pd.DataFrame([company_data])
    df.to_csv('company_data.csv', index=False)
    print("Data has been saved to company_data.csv")
else:
    print("No data extracted.")
