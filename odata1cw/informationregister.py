import json

import requests

from odata1cw.core import Infobase
from odata1cw.utils import make_url_part


class InformationRegister:
    infobase: Infobase

    def __init__(self, infobase, regname):
        self.infobase = infobase
        self.regname = regname
        self.url = self.infobase._full_url.format(
            obj='InformationRegister_'+self.regname)

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

    def slice_last(self, **kwargs):
        _url_select = make_url_part('select', kwargs.get('select'), str)
        _url_orderby = make_url_part('orderby', kwargs.get('orderby'), str)
        _url_expand = make_url_part('expand', kwargs.get('expand'), str)
        period_value = '' if kwargs.get('period') is None else kwargs.get('period')
        condition_value = '' if kwargs.get('condition') is None else kwargs.get('condition')

        full_url = (self.infobase._full_url.format(
            obj='InformationRegister_'+self.regname+f'/SliceLast({period_value},{condition_value})'))+f'{_url_select}{_url_orderby}{_url_expand}'

        r = requests.get(full_url, auth=self.infobase._auth,
                         headers=self.infobase._headers)
        if(r.status_code != 200):
            raise Exception(r.text)
        return json.loads(r.text)    
