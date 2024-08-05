import requests
from bs4 import BeautifulSoup
import pandas as pd
# URL of the website

# Fetch the web page
# response = requests.get(url)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the HTML content
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Find all anchor tags
#     links = soup.find_all('a')
    
#     # Extract href attributes and print them
#     for link in links:
#         href = link.get('href')
#         if href:
#             print(href)
# else:
#     print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Function to extract company data from a link
# def extract_company_data(link):
#     response = requests.get(link)
#     if response.status_code == 200:
#         # Adjust the selectors based on the actual structure of the page
#         company_name = soup.find('div', class_='company-name').get_text(strip=True)
#         # while(True)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         mobile_number = soup.find('div', class_='mobile-number').get_text(strip=True)
#         whatsapp_number = soup.find('div', class_='whatsapp-number').get_text(strip=True)
#         return {
#             'company_name': company_name,
#             'mobile_number': mobile_number,
#             'whatsapp_number': whatsapp_number
#         }
#     return None

# Fetch the main web page
hrefs,i=[],1
while(True):
    url = 'https://ed.indexpo.co.in/allexpo/47/22?page={i}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('div', class_="col-lg-6 col-sm-6 col-xs-12",)
        # links.find('div', class_= 'ex-btn')
        # print(links,"---->")
        for link in links:
            # Find the nested div with the class 'ex-btn' within each link
            ex_btn_div = link.find('div', class_='ex-btn')
            if ex_btn_div:
                # Extract the href attribute from an anchor tag inside ex_btn_div
                a_tag = ex_btn_div.find('a', class_='btn btn-primary btn-hover-heading-color')
                if a_tag and 'href' in a_tag.attrs:
                    href = a_tag['href']
                    hrefs.append(href)
        i+=1
        if(i>39):
            break
# print(hrefs)
# print(len(hrefs))

def getValueFromSpan(li):
    span_tag = li.find('span')
    # print(li)
    if span_tag:
        return span_tag.get_text(strip=True)
    
        

# Function to extract company data from the given URL
def extract_company_data(href_url):
    response = requests.get(href_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the company name from the h2 tag inside 'course-details-banner-content' class
        company_name = soup.select_one('div.course-details-banner-content h2').get_text(strip=True)
        
        # Extract mobile number and WhatsApp number from the 'sidebar-description' class
        sidebar = soup.select_one('div.sidebar-description')
        # print(sidebar)
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
# print(len(hrefs))

all_company_data = []
# URL to extract data from
for href_url in hrefs:
    company_data = extract_company_data(href_url)
    if company_data:
        all_company_data.append(company_data)


    # Save the data to a CSV file
if all_company_data:
    df = pd.DataFrame(all_company_data)
    df.to_csv('company_data.csv', index=False)
    print("Data has been saved to company_data.csv")
else:
    print("No data extracted.")
