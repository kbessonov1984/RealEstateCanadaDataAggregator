from REDA.main import ZoloMetaDataPull,getZoloRecodsFromNet,getDetailedZoloListingData

header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

def test_ZoloMetaDataPull():

    address = "4748 Pioneer Trail, Guelph, Ontario"
    zolodict = ZoloMetaDataPull(MLSvalue="30786948", header=header, address=address) #30784864 #X4457153 (Sold) X4670598(For Sale)
    print(zolodict)
    assert zolodict["HomeType"] == "Freehold"


def test_getZoloRecodsFromNet():
    zolodict = getZoloRecodsFromNet(city="guelph")  # 30784864 #X4457153 (Sold) X4670598(For Sale)
    print(zolodict)


def test_getDetailedZoloListingData():
    detailed_url = "https://www.zolo.ca/guelph-real-estate/28-north-street"
    ZoloDict = {}
    getDetailedZoloListingData(detailed_url,ZoloDict)
    print("Test")
