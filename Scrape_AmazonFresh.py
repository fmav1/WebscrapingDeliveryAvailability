import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def Amazon_scraper(postcodeList):
    ''' Searches the amazon url with the deliverable postcodes on them, looks for postcode format
    if a postcode starts with the list of postcodes pulled from amazon url, its assigned deliverable status'''
    url = "https://www.amazon.co.uk/gp/help/customer/display.html?nodeId=202077730"
    headers = { # Originally contained the researcher's name and e-mail 
        'User-Agent': 'UA',
        'From': 'UA@dummy.com'
        }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    AmazonPCs = []
    data = []
    tables = soup.findAll('table', {'class': 'a-bordered'})
    for table in tables:
        table = table.findAll('tr')   
        for row in table:
            row = row.findAll('td')
            for postcode in row:
                text = postcode.text.strip()
    
                is_match = re.findall(r'\b[A-Z]{1,2}[0-9][A-Z0-9]?',text)
                for PC in is_match:
                    AmazonPCs.append(PC)
    AmazonPCspaced = ['{0} '.format(pc) for pc in AmazonPCs]
    tuple_AmazonPCs = tuple(AmazonPCspaced)
    PC_list_upper = [postcode.upper() for postcode in postcodeList]
    for postcode in PC_list_upper:
            if postcode.startswith(tuple_AmazonPCs):
                Deliverable = "Yes"
            else:
                Deliverable = "No"
            data.append({"Postcode" : postcode, "Deliverable": Deliverable})
    df = pd.DataFrame(data)
    df.to_csv('data\PCcheckerAmazon.csv')

