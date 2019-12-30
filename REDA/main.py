import requests
from bs4 import BeautifulSoup
import re, os, datetime


class Home:
    def __init__(self):
        self.realtorurl = ""
        self.zolourl = ""
        self.price = ""
        self.address = ""
        self.type = ""
        self.bedrooms = ""
        self.bathrooms = ""
        self.datetoday = ""
        self.latitude = ""
        self.longitude = ""
        self.neighbourhood = "",
        self.age = "",
        self.size = "",
        self.taxes = "",
        self.daysonmarket = ""



def writeOutResults(dictHomeObjects):
    if os.path.exists("homelistings.txt"):
        fpout = open(file="homelistings.txt", mode="a")
    else:
        fpout = open(file="homelistings.txt",mode="w")


    fpout.write("MLS#\tAddress\tNeighbourhood\tLatitude\tLongitude\tPrice\tSize(sqft)\tTaxes\tAge\tDOM\tType\tBedrooms\tBathrooms\tRealtorURL\t"
                "ZoloURL\tDate\n")
    for MLSvalue in dictHomeObjects.keys():
        fpout.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                            MLSvalue,
                            dictHomeObjects[MLSvalue].address,
                            dictHomeObjects[MLSvalue].neighbourhood,
                            dictHomeObjects[MLSvalue].latitude,
                            dictHomeObjects[MLSvalue].longitude,
                            dictHomeObjects[MLSvalue].price,
                            dictHomeObjects[MLSvalue].size,
                            dictHomeObjects[MLSvalue].taxes,
                            dictHomeObjects[MLSvalue].age,
                            dictHomeObjects[MLSvalue].daysonmarket,
                            dictHomeObjects[MLSvalue].type,
                            dictHomeObjects[MLSvalue].bedrooms,
                            dictHomeObjects[MLSvalue].bathrooms,
                            dictHomeObjects[MLSvalue].realtorurl,
                            dictHomeObjects[MLSvalue].zolourl,
                            dictHomeObjects[MLSvalue].datetoday
                                                              ))





def ZoloMetaDataPull(MLSvalue,header):
    #MLSvalue="30760991"#"X4617994" #30760991
    url="https://www.zolo.ca/index.php?sarea="+MLSvalue+"&filter=1"
    page_html = requests.get(url,headers=header)
    html_soup = BeautifulSoup(page_html.content,"html.parser")

    try:
        status_msg = html_soup.find("div", class_="nearby-container sm-border").find("h4",class_="gut xs-py2 xs-border-bottom").text
        print("MLS#:{}.{}".format(MLSvalue,status_msg))
        return(dict.fromkeys(["ZoloURL","Neighbourhood","Age","Size","Taxes","DaysOnMarket"],"-"))
    except:
        print("Record found for MLS#:{}".format(MLSvalue))
        pass

    hit_html = html_soup.find("ul", class_="listings xs-flex xs-flex-column sm-flex-row sm-flex-wrap list-unstyled").find("li",class_="listing-column text-4")



    try:
        neighbourhood = hit_html.find("span",class_="neighbourhood").text[1:]
        print(neighbourhood)
        #.("span", class_="neighbourhood").text[1:]
    except:
        neighbourhood = "-"
        pass


    detailed_url = hit_html.a["href"]

    #print(url, detailed_url, neighbourhood)


    detailed_html = requests.get(detailed_url,headers=header)
    detailed_listing_soup = BeautifulSoup(detailed_html.content,"html.parser")

    property_details_list = detailed_listing_soup.find("div",class_="column-container sm-column-count-2 column-gap").find_all("dl",class_="column")

    for i in range(0,len(property_details_list)):
        if property_details_list[i].dt.text == "Days on Site":
            DOM = property_details_list[i].dd.text.strip()
    #print(url, detailed_url)
    for i in range(0, len(property_details_list)):
        if property_details_list[i].dt.text == "Year Built" or property_details_list[i].dt.text == "Age":
            homeAge=property_details_list[i].dd.text

    return ({"ZoloURL":detailed_url,
             "Neighbourhood":neighbourhood,
             "Age": homeAge.rstrip(),
             "Size":property_details_list[2].dd.text.rstrip(),
             "Taxes": property_details_list[5].dd.text.rstrip(),
             "DaysOnMarket": DOM}
            )



    #with open(file="zolopage.html", mode="w") as fp:
    #    fp.write(detailed_html.content.decode("utf-8"))

if __name__ == '__main__':
    print("Real Estate Data Aggregator")



    header = {
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
    house_containers = html_soup.find_all('div', class_="smallListingCard")

    for house_container in house_containers:
        MLSvalue=house_container.find_all("div", class_="smallListingCardMLSVal")[0]["title"]

        HomeInstance = Home()

        HomeInstance.realtorurl = house_container.find_all("a",class_="blockLink listingDetailsLink")[0]["href"]
        HomeInstance.price = re.sub("[$|,]+","", house_container.find_all("div", class_="smallListingCardBody")[0].find("div",class_="smallListingCardPrice").text)
        HomeInstance.address = house_container.find_all("div", class_="smallListingCardAddress")[0].text

        lat_long_string = house_container.find_all("a", class_="propertyCardDetailsNoteIcon noteIcon")[0]["data-value"]
        lat_long_tuple = re.match(".*_(\d+\.\d+)_(.*\.\d+)", lat_long_string).group(1, 2)
        HomeInstance.latitude = lat_long_tuple[0]
        HomeInstance.longitude = lat_long_tuple[1]

        #if re.match("#",HomeInstance.address):
        #    continue #skip addresses that start with # sign
        HomeInstance.bedrooms = house_container.find_all("div", class_="smallListingCardIconStrip")[0].find_all("div",class_="smallListingCardIconNum")[0].text
        HomeInstance.bathrooms = house_container.find_all("div", class_="smallListingCardIconStrip")[0].find_all("div",class_="smallListingCardIconNum")[1].text

        if re.match(".*single-family.*", HomeInstance.realtorurl):
            HomeInstance.type="Single Family"
        elif re.match(".*condo.*", HomeInstance.realtorurl):
            HomeInstance.type="Condo"
        else:
            HomeInstance="Unknown"

        HomeInstance.datetoday=str(datetime.date.today())

        ZoloMetaDict = ZoloMetaDataPull(MLSvalue=MLSvalue, header=header)

        if ZoloMetaDict:
            HomeInstance.zolourl = ZoloMetaDict["ZoloURL"]
            HomeInstance.neighbourhood = ZoloMetaDict["Neighbourhood"]
            HomeInstance.age = ZoloMetaDict["Age"]
            HomeInstance.size = ZoloMetaDict["Size"]
            HomeInstance.taxes = ZoloMetaDict["Taxes"]
            HomeInstance.daysonmarket = ZoloMetaDict["DaysOnMarket"]


        #print(MLSvalue, HomeInstance.address, HomeInstance.price, HomeInstance.bedrooms, HomeInstance.bathrooms)
        dictHomeObjects[MLSvalue]= HomeInstance


    writeOutResults(dictHomeObjects)

    print("Done parsing")


#add Zolo to get additional details
# Get listing URL https://www.zolo.ca/index.php?sarea=30775035&filter=1
# https://www.zolo.ca/guelph-real-estate/31-schroder-crescent