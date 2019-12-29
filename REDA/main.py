import requests
from bs4 import BeautifulSoup
import re

class Home:
    def __init__(self):
        self.url = ""
        self.price = ""
        self.address = ""
        self.type = ""
        self.bedrooms = ""
        self.bathrooms = ""

def writeOutResults(dictHomeObjects):
    with open(file="homelistings.txt",mode="w") as fpout:
        fpout.write("MLS#\tAddress\tPrice\tType\tBedrooms\tBathrooms\tURL\n")
        for MLSvalue in dictHomeObjects.keys():
            fpout.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(MLSvalue,
                                              dictHomeObjects[MLSvalue].address,
                                              dictHomeObjects[MLSvalue].price,
                                              dictHomeObjects[MLSvalue].type,
                                              dictHomeObjects[MLSvalue].bedrooms,
                                              dictHomeObjects[MLSvalue].bathrooms,
                                              dictHomeObjects[MLSvalue].url
                                              ))


if __name__ == '__main__':
    print("Real Estate Data Aggregator")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    dictHomeObjects={}

    #page_link = 'https://www.realtor.ca/map#ZoomLevel=12&Center=43.534385%2C-80.240165&LatitudeMax=43.60018&LongitudeMax=-80.06988&LatitudeMin=43.46852&LongitudeMin=-80.41045&Sort=1-A&PGeoIds=g30_dpwzwhvk&GeoName=Guelph%2C%20ON&PropertyTypeGroupID=1&PropertySearchTypeId=1&TransactionTypeId=2&Currency=CAD'


    #https://www.realtor.ca/map#ZoomLevel=12&Center=43.534385%2C-80.240165&LatitudeMax=43.60018&LongitudeMax=-80.06988
    # &LatitudeMin=43.46852&LongitudeMin=-80.41045&Sort=1-A
    # &PGeoIds=g30_dpwzwhvk&GeoName=Guelph%2C%20ON&PropertyTypeGroupID=1&PropertySearchTypeId=1&TransactionTypeId=2&Currency=CAD

    # this is the url that we've already determined is safe and legal to scrape from.
    #page_response = requests.get(page_link,headers)
    #print(page_response.content)

    # here, we fetch the content from the url, using the requests library
    #page_content = BeautifulSoup(page_response.content, "html.parser")
    with open(file="page.html", mode="r") as fp:
        page_html = fp.read()
    html_soup = BeautifulSoup(page_html, "html.parser")
    house_containers = html_soup.find_all('a', class_="blockLink listingDetailsLink")

    for house_container in house_containers:
        MLSvalue=house_container.find_all("div", class_="smallListingCardMLSVal")[0]["title"]

        HomeInstance = Home()
        HomeInstance.url= house_container["href"]
        HomeInstance.price = re.sub("[$|,]+","", house_container.find_all("div", class_="smallListingCardBody")[0].find("div",class_="smallListingCardPrice").text)
        HomeInstance.address = house_container.find_all("div", class_="smallListingCardAddress")[0].text


        if re.match("#",HomeInstance.address):
            continue #skip addresses that start with # sign
        HomeInstance.bedrooms = house_container.find_all("div", class_="smallListingCardIconStrip")[0].find_all("div",class_="smallListingCardIconNum")[0].text
        HomeInstance.bathrooms = house_container.find_all("div", class_="smallListingCardIconStrip")[0].find_all("div",class_="smallListingCardIconNum")[1].text

        if re.match(".*single-family.*", HomeInstance.url):
            HomeInstance.type="Single Family"
        elif re.match(".*condo.*", HomeInstance.url):
            HomeInstance.type="Condo"
        else:
            HomeInstance="Unknown"

        #print(MLSvalue, HomeInstance.address, HomeInstance.price, HomeInstance.bedrooms, HomeInstance.bathrooms,  HomeInstance.url)
        dictHomeObjects[MLSvalue]= HomeInstance


    writeOutResults(dictHomeObjects)
    # we use the html parser to parse the url content and store it in a variable.
    textContent = []
