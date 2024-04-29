import requests


class WMS:
    def __init__(self, ):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Connection': 'keep-alive'
        }
        self.server = '172.172.185.67'
        self.infobase = 'krd_itc_wms'
        self.username = 'ODUser'
        self.password = 249981
        self.params = None
        self.full_url = f"http://{self.server}/{self.infobase}/odata/standard.odata/"
        self._auth = requests.auth.HTTPBasicAuth(self.username, self.password)

    def connect(self, _top=None):

        if _top is not None:
            if self.params is None:
                self.params = f"$top={_top}"
            else:
                self.params = f"{self.params}&$top={_top}"
        response = requests.get(url=self.full_url, headers=self.headers, auth=self._auth, params=self.params)
        return response
