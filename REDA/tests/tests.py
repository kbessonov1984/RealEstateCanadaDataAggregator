from REDA.main import ZoloMetaDataPull


def test_ZoloMetaDataPull():
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    zolodict = ZoloMetaDataPull(MLSvalue="X4670598", header=header)
    assert zolodict["HomeType"] == "Single Family"