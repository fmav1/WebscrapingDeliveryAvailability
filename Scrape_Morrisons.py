import requests
import pandas as pd
from bs4 import BeautifulSoup

postcodes = ['AB140TT', 'SW1A 0AA', 'L4 0TH', 'G62 1ER', "gibber ish", "S11 8EQ"]

def Morrisons_scraper(postcodeList):
    '''Simple GET request on the morrisons website, parsing the result into BeautifulSoup then returning the delivery status'''
    data = []
    headers = { # Originally contained the researcher's name and e-mail 
        'User-Agent': 'UA',
        'From': 'UA@dummy.com'
        }
    for postcode in postcodeList:
        url = "https://accounts.groceries.morrisons.com/auth-service/sso/register?postcode=" + postcode
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.text
        if "Great news" in result:
            status = "Yes"
            Deliverable = "Yes"
        elif "not delivering to your area just yet" in result: 
            status = "Not delivering yet"
            Deliverable = "No"
        else:
            status = "That postcode doesn't seem right"
            Deliverable = "No"
        data.append({"Postcode" : postcode, "Status" : status, "Deliverable": Deliverable})
    df = pd.DataFrame(data)
    df.to_csv('data\PCcheckerMorrisons.csv')
