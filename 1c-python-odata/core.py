import json
import requests


class InfoBase:
    server: str
    infobase: str
    _full_url: str
    _auth: str
    _headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Connection': 'keep-alive'
    }

    def __init__(self, server, infobase, username, password):
        self.server = server
        self.infobase = infobase

        self._full_url = server + infobase + \
            '/odata/standard.odata/{obj}?$format=json'
        self._auth = requests.auth.HTTPBasicAuth('IBelov', '1722199')

    def metadata(self):
        url = self._full_url.format(obj='')
        r = requests.get(url, auth=self._auth, headers=self._headers)
        if(r.status_code != 200):
            raise Exception(r)

        return r.text

    def _make_url_part(self, name, value, value_type):
        if value == None:
            return ''
        if type(value) != value_type:
            raise ValueError('{}={} must be {}'.format(
                name, value, value_type))
        result = "&${}={}".format(name, value)
        return result

    def get_documents(self, name, top=None, skip=None, select=None, odata_filter=None):
        url = self._full_url.format(obj='Document_'+name)
        _url_top = self._make_url_part('top', top, int)
        _url_skip = self._make_url_part('skip', skip, int)
        _url_select = self._make_url_part('select', select, str)
        _url_filter = self._make_url_part('filter', odata_filter, str)

        url = url + _url_top + _url_skip + _url_select + _url_filter

        r = requests.get(url, auth=self._auth, headers=self._headers)
        if(r.status_code != 200):
            raise Exception
        return json.loads(r.text)['value']
