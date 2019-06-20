import json

import requests

from odata1cw.core import Infobase
from odata1cw.utils import make_url_part


class Catalog:
    infobase: Infobase

    def __init__(self, infobase, catname):
        self.infobase = infobase
        self.catname = catname
        self.url = self.infobase._full_url.format(obj='Catalog_'+self.catname)

    def get(self, guid, select=None):
        obj = "Catalog_{}(guid'{}')".format(self.catname, guid)
        url = self.infobase._full_url.format(obj=obj)
        _url_select = make_url_part('select', select, str)
        url = url + _url_select
        r = requests.get(url, auth=self.infobase._auth,
                         headers=self.infobase._headers)
        if(r.status_code != 200):
            raise Exception(r.text)
        return json.loads(r.text)

    def query(self, top=None, skip=None, select=None, odata_filter=None, expand=None):
        _url_top = make_url_part('top', top, int)
        _url_skip = make_url_part('skip', skip, int)
        _url_select = make_url_part('select', select, str)
        _url_filter = make_url_part('filter', odata_filter, str)
        _url_expand = make_url_part('expand', expand, str)
        url = self.url + _url_top + _url_skip + _url_select + _url_filter + _url_expand
        r = requests.get(url, auth=self.infobase._auth,
                         headers=self.infobase._headers)
        if(r.status_code != 200):
            raise Exception(r.text)
        return json.loads(r.text)['value']

    def create(self, data):
        r = requests.post(self.url, auth=self.infobase._auth,
                          headers=self.infobase._headers, data=json.dumps(data))
        if r.status_code != 201:
            raise Exception(r.text)
        return json.loads(r.text)

    def edit(self, guid, data):
        obj = "Catalog_{}(guid'{}')".format(self.catname, guid)
        url = self.infobase._full_url.format(obj=obj)
        r = requests.patch(url, auth=self.infobase._auth,
                           headers=self.infobase._headers, data=json.dumps(data))
        if(r.status_code != 200):
            raise Exception(r.text)

        return json.loads(r.text)
