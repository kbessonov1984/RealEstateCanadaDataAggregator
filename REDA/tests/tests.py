from REDA.main import ZoloMetaDataPull,getZoloRecodsFromNet

header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

def test_ZoloMetaDataPull():

    address = "35 -  714 WILLOW Road, Guelph, Ontario"
    zolodict = ZoloMetaDataPull(MLSvalue="X4674674", header=header, address=address) #30784864 #X4457153 (Sold) X4670598(For Sale)
    print(zolodict)
    assert zolodict["HomeType"] == "Freehold"


def test_getZoloRecodsFromNet():
    zolodict = getZoloRecodsFromNet(city="guelph")  # 30784864 #X4457153 (Sold) X4670598(For Sale)
    print(zolodict)