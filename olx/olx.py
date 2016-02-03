#!/usr/bin/env python3
import re
import json
import requests
from bs4 import BeautifulSoup as b

pages = 1  # How many pages should be scraped

#catURL = "http://olx.ro/oferte/q-vinil/"
catURL = "http://olx.ro/imobiliare/cluj-napoca/q-observator/"

# Links to the Ajax requests
ajaxNum = "http://olx.ro/ajax/misc/contact/phone/"
ajaxYah = "http://olx.ro/ajax/misc/contact/communicator/"

### Get the name from the ad
def getName(link):
    page = requests.get(link)
    #get the HTML content
    soup = b(page.text,"html.parser")
    #return the html element containing the name. eq: <span class="block color-5 brkword xx-large">Franc</span>
    nameMatch = soup.find(attrs={"class": "block color-5 brkword xx-large"})

    priceMatchTemp = soup.find('strong',{"class": "xxxx-large margintop7 block not-arranged"})
    if priceMatchTemp == None:
        priceMatch = soup.find('strong',{"class": "xxxx-large margintop7 block arranged"})
    else:
        priceMatch=priceMatchTemp

    #return the name
    name = re.search(">(.+)<", str(nameMatch)).group(1)
    price = re.search(">(.+)<", str(priceMatch)).group(1)
    return name,price


def getPhone(itemID):
    resp = requests.get("%s%s/" % (ajaxNum, itemID)).text
    try:
        resp = json.loads(resp).get("value")
    except ValueError:
        return None  # No phone number
    return resp


def getYahoo(itemID):
    # Get the Yahoo! ID
    resp = requests.get("%s%s/" % (ajaxYah, itemID)).text
    try:
        resp = json.loads(resp).get("value")
    except ValueError:
        return None
    else:
        return resp

def main():
    for pageNum in range(1, pages+1):
        print("Page %d." % pageNum)
        page = requests.get(catURL + "?page=" + str(pageNum))
        soup = b(page.text,"html.parser")
        links = soup.findAll(attrs={"class":
                                    "marginright5 link linkWithHash \
                                    detailsLink"})

        for item in links:
             #print(item)
             itemID = re.search('ID(.+)\.', item['href']).group(1)
             print("ID: %s" % itemID)
             title=re.search('<strong>(.+)</strong>', str(item)).group(1)
             print("\tTitle: %s" % title)
             print("\tPrice: %s" % getName(item['href'])[1])
             print("\tName: %s" % getName(item['href'])[0])
             phoneNumber=getPhone(itemID)
             yahooID=getYahoo(itemID)
             if phoneNumber != None:
                 print("\tPhone: %s" % phoneNumber)
             if  yahooID!= None:
                 print("\tYahoo: %s" % yahooID)

if __name__ == "__main__":
    main()
