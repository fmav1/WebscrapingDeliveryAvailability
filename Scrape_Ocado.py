import requests
import pandas as pd
from bs4 import BeautifulSoup

postcodes = ['SE1 9SG', 'SW1A 0AA', 'G62 1ER', 'S11 8EQ', 'LS10 1ER', "gibberish", 'L4 0TH']
 
def Ocado_scraper(postcodeList):
    ''' Starts up a request session, POSTs the postcode in the payload, parsing the result to BS4 then returning the delivery
    status'''
    data = []
    headers = { # Originally contained the researcher's name and e-mail 
        'User-Agent': 'UA',
        'From': 'UA@dummy.com'
        }
    for postcode in postcodeList:
        session = requests.Session()
        payload = {'postcode': postcode}
        reqUrl = 'https://www.ocado.com/webshop/postcodeCheckPerform.do'
        r = session.post(reqUrl,data=payload,headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.find_all("h3")[1].text
        if "Yay" in result:
            status = "Yes"
            Deliverable = "Yes"
        elif "We'll be there soon" in result:
            status = "Soon"
            Deliverable = "No"
        elif "We're having trouble" in result:
            status = "Having trouble confirming postcode"
            Deliverable = "No"
        elif "Do we deliver to you?" in result:
            status = "Invalid postcode"
            Deliverable = "No"
        data.append({"Postcode" : postcode, "Status" : status, "Deliverable": Deliverable})
    df = pd.DataFrame(data)
    df.to_csv('data\PCcheckerOcado.csv')
    # Optional parameter change variable r
    # cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
    # r = session.post(reqUrl,data=payload,cookies =cookies)
