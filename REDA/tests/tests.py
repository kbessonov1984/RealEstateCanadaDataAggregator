from REDA.main import ZoloMetaDataPull


def test_ZoloMetaDataPull():
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    address = "35 -  714 WILLOW Road, Guelph, Ontario"
    zolodict = ZoloMetaDataPull(MLSvalue="30779762", header=header, address=address) #30784864 #X4457153 (Sold) X4670598(For Sale)
    print(zolodict)
    assert zolodict["HomeType"] == "Freehold"