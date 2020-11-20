import requests
import pandas as pd
from bs4 import BeautifulSoup

postcodes = ['SE1 9SG', 'SW1A 0AA', 'L4 0TH', 'G62 1ER', "gibber ish", "S11 8EQ"]

def ASDA_scraper(postcodeList):
    '''Simple postcode scraper using ASDAs API. Goes through list of postcodes, pulls the result, if positive
    then assigned deliverable status'''
    data = []
    headers = { # Originally contained the researcher's name and e-mail 
        'User-Agent': 'UA',
        'From': 'UA@dummy.com'
        }
    for postcode in postcodeList:
        url = "https://groceries.asda.com/api/user/checkpostcode?listcnc=true&responsegroup=extended&postcode=" + postcode
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.text
        #print (result)
        if "Good news" in result:
            status = "Yes"
            Deliverable = "Yes"
        elif "don't deliver to" in result: 
            status = "Do not currently deliver"
            Deliverable = "No"
        else:
            status = "That postcode doesn't seem right"
            Deliverable = "No"
        data.append({"Postcode" : postcode, "Status" : status, "Deliverable": Deliverable})
    df = pd.DataFrame(data)
    df.to_csv('data\PCcheckerASDA.csv')
        
