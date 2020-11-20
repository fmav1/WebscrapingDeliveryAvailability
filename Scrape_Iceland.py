import requests
import pandas as pd
from bs4 import BeautifulSoup

postcodes = ['SE1 9SG', 'SW1A 0AA', 'G62 1ER', 'S11 8EQ', 'IV24 3BW', "gibberish", 'L4 0TH']

def Iceland_scraper(postcodeList):
    ''' The function acquires the csrf token from the home page, then makes a POST request on the delivery status.
    The client starts up a session, enters the payload with the postcode then returns the delivery status.'''
    data = []
    headers = { # Originally contained the researcher's name and e-mail 
        'User-Agent': 'UA',
        'From': 'UA@dummy.com'
        }
    url = 'https://www.iceland.co.uk/book-delivery?shopping=false'
    post_url = "https://www.iceland.co.uk/on/demandware.store/Sites-icelandfoodsuk-Site/default/Delivery-UpdateAddress"
    for postcode in postcodeList:
        client = requests.Session()
        r = BeautifulSoup(client.get(url).text, "html.parser")
        csrf_token = r.findAll('input', {'name':'csrf_token'})[1].get('value') 
        payload = {'dwfrm_singleshipping_shippingAddress_addressFields_postal': postcode,
               'dwfrm_singleshipping_shippingAddress_addressFields_checkPostcode': 'Edit postcode',
               'csrf_token': csrf_token
               }  
        z = client.post(post_url, data=payload, headers=headers)
        soup = BeautifulSoup(z.text, 'lxml')
        result = soup.find_all("span")
        for status in result:
            if "unable to deliver to" in status.text:
                Deliverable = "No"
            elif "First available delivery time!" in status.text:
                Deliverable = "Yes"
        data.append({"Postcode" : postcode, "Deliverable": Deliverable})   
    df = pd.DataFrame(data)
    df.to_csv('data\PCcheckerIceland.csv')


  


    
    
    
    