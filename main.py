from bs4 import BeautifulSoup

import requests
import pandas as pd
import numpy as np


# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find('span', attrs={'id': 'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price

def get_price(soup):

    try:
        price = soup.find('span', attrs={'class': 'a-offscreen'}).text.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find('span', attrs={'class': 'a-offscreen'}).text.strip()

        except:
            price = ""

    return price
# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find('span', attrs={'class': 'a-icon-alt'}).text.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available



if __name__ == '__main__':

    # add your user agent 
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.amazon.com/s?k=playstation&i=sporting-intl-ship&crid=3NDPSOHIIEXKT&sprefix=playstation%2Csporting-intl-ship%2C575&ref=nb_sb_noss_2"
    #https://www.amazon.com/s?k=playstation&i=sporting-intl-ship&crid=3NDPSOHIIEXKT&qid=1684840785&sprefix=playstation%2Csporting-intl-ship%2C575&ref=sr_pg_1
    #https://www.amazon.com/s?k=playstation&i=sporting-intl-ship&page=3&crid=3NDPSOHIIEXKT&qid=1684840785&sprefix=playstation%2Csporting-intl-ship%2C575&ref=sr_pg_3
    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
    
    # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)

    print(amazon_df)

    















# print("Put some skill that you are not familiar with" )
# unfamiliar_skill = input('>')
# print(f'Filtering Out {unfamiliar_skill}')

# def find_jobs():

# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
#     'Accept-Language': 'en-US, en;q=0.5'
# }

# webpage = requests.get('https://www.amazon.com/s?k=playstation&i=sporting-intl-ship&crid=3NDPSOHIIEXKT&sprefix=playstation%2Csporting-intl-ship%2C575&ref=nb_sb_noss_2', headers=HEADERS )
# soup = BeautifulSoup(webpage.content, 'html.parser')

# links = soup.find_all('a', attrs='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
# link = links[0].get('href')
# product_list = 'https://www.amazon.com' + link


# new_webpage = requests.get(product_list, headers=HEADERS)
# new_soup = BeautifulSoup(new_webpage.content, 'html.parser')
# new_soup.find('span', attrs={'id': 'productTitle'}).text.strip()
# new_soup.find('span', attrs={'class': 'a-offscreen'}).text.strip()
# new_soup.find('span', attrs={'class': 'a-icon-alt'}).text







#     for index, job in enumerate(jobs):
#         company_name = job.find('img', class_="s-image").text.replace(' ', '')
#         skills = job.find('span', class_="a-size-base-plus a-color-base a-text-normal").text.replace(' ', '')
        
#         more_info = job.find('span', class_="a-icon-alt").text.replace(' ', '')
        
#         with open(f'posts/{index}.txt', 'w') as f:
#             f.write(f"Company Name: {company_name.strip()} \n")
#             f.write(f"Required Skills: {skills.strip()} \n")
#             f.write(f"More Info: {more_info}")

#         print(f"File saved: {index}")

      

# if __name__ == '__main__':
#     while True: 
#         find_jobs()
#         time_wait = 10
#         print(f'waiting {time_wait} minutes...')
#         time.sleep(time_wait * 60 ) 