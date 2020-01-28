import requests
from bs4 import BeautifulSoup
import re, os, datetime
__version__="1.1.0"

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
        self.daysonmarket = "",
        self.soldprice = "",
        self.status = "",




def writeOutResults(dictHomeObjects):
    if os.path.exists("homelistings.txt"):
        fpout = open(file="homelistings.txt", mode="a")
    else:
        fpout = open(file="homelistings.txt",mode="w")
        fpout.write("MLS#\tAddress\tNeighbourhood\tLatitude\tLongitude\tPrice\tSize(sqft)\tTaxes\tAge\tDOM\tType\tBedrooms\tBathrooms\tRealtorURL\t"
                "ZoloURL\tDate\tStatus\tSoldPrice\n")

    for MLSvalue in dictHomeObjects.keys():
        fpout.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
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
                            dictHomeObjects[MLSvalue].datetoday,
                            dictHomeObjects[MLSvalue].status,
                            dictHomeObjects[MLSvalue].soldprice
                                                              ))

    print("Wrote final results to the {}".format(os.path.join(os.getcwd(),"homelistings.txt")))



def ZoloMetaDataPull(MLSvalue,header,address):
    #MLSvalue="30760991"#"X4617994" #30760991
    ZoloDict = dict.fromkeys(["ZoloURL", "Neighbourhood", "Age",
                   "Size", "Taxes", "DaysOnMarket", "DatePosted",
                   "PropertyType", "HomeType",
                   "Status", "SoldPrice", "SoldDate", "Price",
                   "Latitude", "Longitude", "Bedrooms","Bathrooms"], "-")

    url="https://www.zolo.ca/index.php?sarea="+MLSvalue+"&filter=1"

    page_html = requests.get(url, headers=header)
    html_soup = BeautifulSoup(page_html.content,"html.parser")


    try:
        status_msg = html_soup.find("div", class_="nearby-container sm-border").find("h4",class_="gut xs-py2 xs-border-bottom").text
        print("MLS#:{}.{}".format(MLSvalue,status_msg))
    except:
        status_msg=""; pass

    if status_msg == "Oops! No homes match your search.":
        unit=None; streetnum=None; streetname=None;
        print(address)
        patterns={"freehold": r"^(\d+)\s+(.+),\s+(.+),\s+(.+)",
                  "condo": r"#?(\d+)\s+(\-\s{0,})(\d+)\s+(.+),\s+(.+),\s+(.+)"
                  }
        for key in patterns.keys():
            addressmatches = re.match(patterns[key], address)
            if addressmatches and key == "condo":
                addressmatches = addressmatches.groups()
                unit = int(addressmatches[0])
                streetnum = int(addressmatches[2])
                streetname = re.sub(" ", "-", addressmatches[3])
                city = addressmatches[4]

            elif addressmatches and key == "freehold":
                addressmatches = addressmatches.groups()  # freehold match
                streetnum = int(addressmatches[0])  # tests if street number is correctly parsed
                streetname = re.sub(" ", "-", addressmatches[1]);
                city = addressmatches[2]
                if re.search(r"\d+",streetname):
                    continue
                else:
                    break

        print(addressmatches)


        if unit and streetnum and streetname:
            detailed_url = "https://www.zolo.ca/" + city + "-real-estate/" + str(streetnum) + "-" + streetname+"/"+str(unit)
        elif streetnum and streetname:
            detailed_url = "https://www.zolo.ca/"+ city +"-real-estate/"+str(streetnum)+"-"+streetname
        else:
            return( ZoloDict )
    else:
        print("Record found for MLS#:{}".format(MLSvalue));
        hit_html = html_soup.find("ul", class_="listings xs-flex xs-flex-column sm-flex-row sm-flex-wrap list-unstyled").find("li",class_="listing-column text-4")
        detailed_url=""
        for link in hit_html.find_all("a"):
            if re.match("https://www.zolo",link["href"]):
                detailed_url=link["href"]
                break
        #detailed_url = hit_html.a["href"]
        #print(detailed_url,address,hit_html);
        if detailed_url == "":
            return(ZoloDict)

    #detailed listing pooling for detailed url
    neighbourhood="-"

    print(detailed_url)
    #detailed_url = "https://www.zolo.ca/guelph-real-estate/111-moss-place"
    detailed_html = requests.get(detailed_url,headers=header)
    detailed_listing_soup = BeautifulSoup(detailed_html.content,"html.parser")

    try:
        property_details_list = detailed_listing_soup.find("div",class_="column-container sm-column-count-2 column-gap").find_all("dl",class_="column")
    except:
        property_details_list=[]
        pass

    try:
        status_price_section = detailed_listing_soup.find("section", class_="listing-price sm-text-right xs-flex-order-2").find_all("div")
    except:
        ZoloDict["ZoloURL"] = detailed_url
        return( ZoloDict )

    #if status section is in Sold property state
    try:
        askprice = int(re.sub(r"\$|,","",status_price_section[0].find("span").text))
    except:
        askprice = 0


    property_status = "";soldprice = "";solddate = "";soldprice = "";
    if any([re.match("Sold",element.text) != None for element in status_price_section]):
        property_status="Sold"
        for i in range(0,len(status_price_section)):
            item = status_price_section[i]
            if re.match(r"\$\d+\w+\d+",item.text) and i==0:
                soldprice = int(re.sub(",","",item.span.text))
            elif re.match("Listed",item.text) and i==1:
                listedprice = int(re.sub(r"\$|,","",item.span.text))
            elif re.match("Sold",item.text) and i==2:
                solddate = item.span.text
    elif any([re.match("Added",element.text) != None for element in status_price_section]):
        property_status = "For Sale"

    DOM=""; DatePosted="";homeAge=""; hometype="Freehold";
    for i in range(0,len(property_details_list)):
        print(property_details_list[i].dt.text, property_details_list[i].dd.text)
        if property_details_list[i].dt.text == "Days on Site":
            DOM = property_details_list[i].dd.text.strip()
            DatePosted = re.match(r"(\d+\s+\()(\w+\s+\d+,\s+\d+)",DOM).group(2)
        if property_details_list[i].dt.text == "Year Built" or property_details_list[i].dt.text == "Age":
            homeAge = property_details_list[i].dd.text
        if re.match("condo", property_details_list[i].dd.text, re.IGNORECASE) or \
            re.match("Strata", property_details_list[i].dt.text):
                hometype = "Condo"



    property_other_details=detailed_listing_soup.find("section",class_="sm-mb3 sm-column-count-2 column-gap").find_all("div")
    for i in range(0, len(property_other_details)):
        item = property_other_details[i]
        if(item.text == "Community"):
            neighbourhood = property_other_details[i+1].span.text

    ZoloDict = {"ZoloURL":detailed_url,
             "Neighbourhood":neighbourhood,
             "Price": askprice,
             "Age": homeAge.rstrip(),
             "Size":property_details_list[2].dd.text.rstrip(),
             "Taxes": re.sub("\n", "", property_details_list[5].dd.text.rstrip()),
             "DaysOnMarket": DOM,
             "DatePosted": DatePosted,
             "HomeType": hometype,
             "Status": property_status,
             "SoldPrice": soldprice,
             "SoldDate": solddate}

    print(ZoloDict)
    return ( ZoloDict )

def getPreviousRecordsFromFile():
    keys=[]
    if os.path.exists("homelistings.txt"):
        with open("homelistings.txt", "r") as fp:
            for line in fp.readlines()[1:]:
                keys.append(line.split("\t")[0])
    MLSvaluesPrevDict=dict.fromkeys(keys,"")
    return(MLSvaluesPrevDict)

    #with open(file="zolopage.html", mode="w") as fp:
    #    fp.write(detailed_html.content.decode("utf-8"))

def getZoloRecodsFromNet(city="guelph"):
    print("Get all current records from the Internet")
    listings_html = [];
    MLS_detail_url_dict = {}

    for i in range(1,20):
        url = "https://www.zolo.ca/"+city+"-real-estate/page-"+str(i)
        print("Scanning Zolo page at {}".format(url))
        zolo_page_html = requests.get(url)
        html_soup = BeautifulSoup(zolo_page_html.content, "html.parser")
        if html_soup:
            listings_html = listings_html + html_soup.find_all("li", class_="listing-column text-4")
        else:
            break
    print("Extracted {} listings".format(len(listings_html)))

    #/html/body/div[1]/main/section[2]/div/ul/li[1]/article/div[1]/ul/li[2]
    for listing in listings_html:
            MLSbaths = "-"; MLSbedrooms = "-"
            MLSlatitude = listing.find_all("meta")[0]["content"]
            MLSlongitude = listing.find_all("meta")[1]["content"]
            listing_url = listing.article.find("a")["href"]

            try:
                MLSbedrooms = re.match(r"^(.+)\s+\w+", listing.find_all("li")[1].text).group(1)
                MLSbaths = re.match(r"^.+(\d+)\s+\w+", listing.find_all("li")[2].text).group(1)
                MLS_street = listing.article.find_all("div")[0].find("span", class_="street").text
                MLS_city = listing.article.find_all("div")[0].find("span", class_="city").text
                MLS_province = listing.article.find_all("div")[0].find("span", class_="province").text
                MLSstring = listing.article.find_all("a")[1].find("img")["alt"]
            except Exception as error:
                print("Exception for url {} and error {}".format(listing_url, error))


            MLS = re.match(r"^.+MLS:\s+(.+)",MLSstring).group(1)
            MLS_detail_url_dict[MLS] = {"url":"","address":""}
            MLS_detail_url_dict[MLS]["url"] = listing_url
            MLS_detail_url_dict[MLS]["latitude"] = MLSlatitude
            MLS_detail_url_dict[MLS]["longitude"] = MLSlongitude
            MLS_detail_url_dict[MLS]["baths"] = MLSbaths
            MLS_detail_url_dict[MLS]["bedrooms"] = MLSbedrooms
            #Housetype = re.match(r"^(\w+)\s+.+", MLSstring).group(1) #House or Condo
            #Housetype = re.sub(r"^(?!Condo).+", "Freehold", Housetype)

            MLS_address = MLS_street+", "+MLS_city+", "+MLS_province
            MLS_detail_url_dict[MLS]["address"] = MLS_address

    return (MLS_detail_url_dict)


if __name__ == '__main__':
    print("Real Estate Data Aggregator version {}".format(__version__))



    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }



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
    if os.path.exists("page.html"):
        with open(file="page.html", mode="r") as fp:
            page_html = fp.read()
        html_soup = BeautifulSoup(page_html, "html.parser")
        house_containers = html_soup.find_all('div', class_="smallListingCard")  # from the realtor.hmtl file
    else:
        house_containers = [] #empty



    for house_container in house_containers:
        MLSvaluePrevious = getPreviousRecordsFromFile()

        MLSvalue = house_container.find_all("div", class_="smallListingCardMLSVal")[0]["title"]

        if MLSvalue in MLSvaluePrevious.keys():
            print("MLSvalue {} already exists in homelistings.txt file. Skipping ...".format(MLSvalue))
            continue


        HomeInstance = Home()


        HomeInstance.realtorurl = str(house_container.find_all("a",class_="blockLink listingDetailsLink")[0]["href"])
        HomeInstance.price = int(re.sub("[$|,]+","", house_container.find_all("div", class_="smallListingCardBody")[0].find("div",class_="smallListingCardPrice").text))
        HomeInstance.address = str(house_container.find_all("div", class_="smallListingCardAddress")[0].text).strip()

        lat_long_string = house_container.find_all("a", class_="propertyCardDetailsNoteIcon noteIcon")[0]["data-value"]
        lat_long_tuple = re.match(r".*_(\d+\.\d+)_(.*\.\d+)", lat_long_string).group(1, 2)

        HomeInstance.latitude = float(lat_long_tuple[0])
        HomeInstance.longitude = float(lat_long_tuple[1])


        #if re.match("#",HomeInstance.address):
        #    continue #skip addresses that start with # sign
        HomeInstance.bedrooms = str(house_container.find_all("div", class_="smallListingCardIconStrip")[0].find_all("div",class_="smallListingCardIconNum")[0].text)
        HomeInstance.bathrooms = str(house_container.find_all("div", class_="smallListingCardIconStrip")[0].find_all("div",class_="smallListingCardIconNum")[1].text)

		#try to get property type by the realtor.ca url
        if re.match(".*single-family.*", HomeInstance.realtorurl):
            HomeInstance.type="Freehold"
        elif re.match(".*condo.*", HomeInstance.realtorurl):
            HomeInstance.type="Condo"
        else:
            HomeInstance.type="Unknown"

        HomeInstance.datetoday = datetime.date.today()

        ZoloMetaDict = ZoloMetaDataPull(MLSvalue=MLSvalue, header=header, address=HomeInstance.address)
        if HomeInstance.type == "Unknown" and ZoloMetaDict["HomeType"] != "-":
            HomeInstance.type=ZoloMetaDict["HomeType"]

        if ZoloMetaDict:
            HomeInstance.zolourl = ZoloMetaDict["ZoloURL"]
            HomeInstance.neighbourhood = ZoloMetaDict["Neighbourhood"]
            HomeInstance.age = ZoloMetaDict["Age"]
            HomeInstance.size = ZoloMetaDict["Size"]
            HomeInstance.taxes = ZoloMetaDict["Taxes"]
            HomeInstance.daysonmarket = ZoloMetaDict["DaysOnMarket"]
            HomeInstance.status = ZoloMetaDict["Status"]
            HomeInstance.soldprice = ZoloMetaDict["SoldPrice"]


        #print(MLSvalue, HomeInstance.address, HomeInstance.price, HomeInstance.bedrooms, HomeInstance.bathrooms)
        dictHomeObjects[MLSvalue]= HomeInstance


    MLSCityZoloDict = getZoloRecodsFromNet(city = "guelph")

    for MLSvalue in MLSCityZoloDict.keys():
        MLSvaluePrevious = list(getPreviousRecordsFromFile().keys()) + list(dictHomeObjects.keys())


        if MLSvaluePrevious:
            if MLSvalue in MLSvaluePrevious:
                print("MLSvalue {} already exists in pooled data. Skipping ...".format(MLSvalue))
                continue

        HomeInstance = Home()
        HomeInstance.datetoday = datetime.date.today()
        HomeInstance.realtorurl = "-"
        HomeInstance.address = MLSCityZoloDict[MLSvalue]["address"]
        HomeInstance.longitude = MLSCityZoloDict[MLSvalue]["longitude"]
        HomeInstance.latitude = MLSCityZoloDict[MLSvalue]["latitude"]
        HomeInstance.bedrooms = MLSCityZoloDict[MLSvalue]["bedrooms"]
        HomeInstance.bathrooms = MLSCityZoloDict[MLSvalue]["baths"]

        ZoloMetaDict = ZoloMetaDataPull(MLSvalue=MLSvalue, header=header, address=HomeInstance.address)

        if ZoloMetaDict["HomeType"] != "-":
            HomeInstance.type=ZoloMetaDict["HomeType"]

        if ZoloMetaDict:
            HomeInstance.zolourl = ZoloMetaDict["ZoloURL"]
            HomeInstance.neighbourhood = ZoloMetaDict["Neighbourhood"]
            HomeInstance.price = ZoloMetaDict["Price"]
            HomeInstance.age = ZoloMetaDict["Age"]
            HomeInstance.size = ZoloMetaDict["Size"]
            HomeInstance.taxes = ZoloMetaDict["Taxes"]
            HomeInstance.daysonmarket = ZoloMetaDict["DaysOnMarket"]
            HomeInstance.status = ZoloMetaDict["Status"]
            HomeInstance.soldprice = ZoloMetaDict["SoldPrice"]


        dictHomeObjects[MLSvalue] = HomeInstance

    writeOutResults(dictHomeObjects)

    print("Done parsing")


#add Zolo to get additional details
# Get listing URL https://www.zolo.ca/index.php?sarea=30775035&filter=1
# https://www.zolo.ca/guelph-real-estate/31-schroder-crescent