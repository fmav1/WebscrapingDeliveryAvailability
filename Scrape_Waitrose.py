import requests
import pandas as pd
from bs4 import BeautifulSoup

def Waitrose_scraper(postcodeList):
    '''Simple GET request to Waitrose website, passes to BS4, returns delivery status'''
    data = []
    headers = { # Originally contained the researcher's name and e-mail 
        'User-Agent': 'UA',
        'From': 'UA@dummy.com'
        }
    for postcode in postcodeList:
        url = "https://www.waitrose.com/shop/SetPostcodeForBranch?postcode=" + postcode
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.text
        if 'offersDelivery":true' in result:
            Deliverable = "Yes"
        elif 'offersDelivery":false' in result: 
            Deliverable = "No"
        data.append({"Postcode" : postcode, "Deliverable": Deliverable})
    df = pd.DataFrame(data)
    df.to_csv('data\PCcheckerWaitrose.csv')
    

