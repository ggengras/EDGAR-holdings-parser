# Graeme Gengras, May 2018
#
# edgay.py - Functions to interact with EDGAR

import requests
from bs4 import BeautifulSoup

def tickerToCIK(ticker):
    """Takes a mutual fund ticker and returns the associated CIK"""

    # Form URL to search for ticker
    url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" \
          + str(ticker)

    # Get the results
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # There should be a tag with the CIK in it, or else ticker is probably invalid
    try:
        tag = soup.find_all('input', attrs={"name": "CIK"})[0]
    except IndexError:
        return None

    CIK = tag['value']
    return CIK

def cikToName(CIK):
    """Takes a CIK and returns the name of the associated company"""

    # Form URL to search for CIK
    url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" \
          + str(CIK)

    # Get the results
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # There should be a tag with the name in it
    tag = soup.find_all('span', attrs={"class": "companyName"})[0]
    name = tag.contents[0]

    return name

def get13F(CIK):
    """Takes a CIK and returns the most recently filed 13F-HR as raw XML"""

    # Search for 13F forms associated with the given CIK
    url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" \
          + str(CIK) + "&type=13F&dateb=&owner=exclude&count=40"

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Get the first 'documentsbutton' tag because results are chronological
    try:
        doctag = soup.find_all('a', id='documentsbutton')[0]
    except IndexError:
        return [None, None]

    # Go to the page with the link to the 13F on it
    formsURL = "https://www.sec.gov" + doctag['href']
    formPage = requests.get(formsURL)
    soup = BeautifulSoup(formPage.text, "html.parser")

    # Get the accepted filing date
    dateTag = soup.find("div", string="Filing Date").next_sibling.next_sibling
    date = dateTag.string

    # Get the link to the 13F XML file (this gets us to the correct general spot
    # then fish around to find the link)
    tableTag = soup.find_all("td", string="INFORMATION TABLE")

    # For some reason we have to go back two (there's an 'empty' sibling)
    linkTag = tableTag[1].previous_sibling.previous_sibling

    # There should only be one child but I can't figure out an easy way to go
    # directly to a child
    for child in linkTag.children:
        linkEnding = child['href']

    xmlLink = "https://www.sec.gov" + linkEnding
    xmlResp = requests.get(xmlLink)

    return [xmlResp.text, date]
