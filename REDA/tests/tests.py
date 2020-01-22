from REDA.main import ZoloMetaDataPull


def test_ZoloMetaDataPull():
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    address = "403 -  45 GOODWIN Drive, Guelph, Ontario"
    zolodict = ZoloMetaDataPull(MLSvalue="30785561", header=header, address=address) #X4457153 (Sold) X4670598(For Sale)
    assert zolodict["HomeType"] == "Freehold"