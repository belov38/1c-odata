import requests



class Infobase:
    _headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }

    server: str
    infobase: str
    _full_url: str
    _auth: str

    def __init__(self, server, infobase, username, password):
        self.server = server
        self.infobase = infobase
        self._full_url = server + infobase + \
            '/odata/standard.odata/{obj}?$format=json'
        self._auth = requests.auth.HTTPBasicAuth(username, password)
