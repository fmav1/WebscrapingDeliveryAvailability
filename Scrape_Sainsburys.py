import requests
import pandas as pd
from bs4 import BeautifulSoup

postcodeList = ['SE1 9SG', 'SW1A 0AA', 'G62 1ER', 'S11 8EQ', "gibberish", 'L4 0TH']

def Sainsburys_scraper(postcodeList):   
    '''Simple PUT request into Sainsburys API with the postcode as the payload, parses to BS4 then returns the result'''
    data = []
    headers = { # Originally contained the researcher's name and e-mail 
        'User-Agent': 'UA',
        'From': 'UA@dummy.com'
        }
    for postcode in postcodeList:
        session = requests.Session()
        payload = {'postcode': postcode}
        reqUrl = 'https://www.sainsburys.co.uk/gol-api/v1/customer/postcode'
        r = session.put(reqUrl,data=payload, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.text
        if "Sorry" in result:
            Deliverable = "No"
        else: 
            Deliverable = "Yes"
        data.append({"Postcode" : postcode, "Deliverable": Deliverable}) 
    df = pd.DataFrame(data)
    df.to_csv('data\PCcheckerSains.csv')
Sainsburys_scraper(postcodeList)