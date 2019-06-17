import json

import requests

from odata1c.core import Infobase
from odata1c.postingmode import PostingMode
from odata1c.utils import make_url_part


class Document:
    infobase: Infobase
    docname: str

    def __init__(self, infobase, docname):
        self.infobase = infobase
        self.docname = docname

    def query(self, top=None, skip=None, select=None, odata_filter=None):
        url = self.infobase._full_url.format(obj='Document_'+self.docname)
        _url_top = make_url_part('top', top, int)
        _url_skip = make_url_part('skip', skip, int)
        _url_select = make_url_part('select', select, str)
        _url_filter = make_url_part('filter', odata_filter, str)

        url = url + _url_top + _url_skip + _url_select + _url_filter

        r = requests.get(url, auth=self.infobase._auth,
                         headers=self.infobase._headers)
        if(r.status_code != 200):
            raise Exception(r.text)
        return json.loads(r.text)['value']

    # TODO documents $count
    # TODO documents $inlinecount
    # TODO documents $orderby
    # TODO documents $expand

    def get(self, guid, select=None):
        obj = "Document_{}(guid'{}')".format(self.docname, guid)
        url = self.infobase._full_url.format(obj=obj)
        _url_select = make_url_part('select', select, str)
        url = url + _url_select
        r = requests.get(url, auth=self.infobase._auth,
                         headers=self.infobase._headers)
        if(r.status_code != 200):
            raise Exception(r.text)
        return json.loads(r.text)

    def post(self, guid, posting_mode):
        obj = "Document_{}(guid'{}')/Post".format(self.docname, guid)
        url = self.infobase._full_url.format(obj=obj)
        if posting_mode == PostingMode.OPER:
            url = url + '&PostingModeOperational=true'
        elif posting_mode == PostingMode.POST:
            url = url + '&PostingModeOperational=false'
        else:
            raise ValueError('Use unpost_document() for unposting')
        r = requests.post(url, auth=self.infobase._auth,
                          headers=self.infobase._headers)
        if(r.status_code != 200):
            raise Exception(r.text)

    def unpost(self, guid):
        obj = "Document_{}(guid'{}')/Unpost".format(self.docname, guid)
        url = self.infobase._full_url.format(obj=obj)
        r = requests.post(url, auth=self.infobase._auth,
                          headers=self.infobase._headers)
        if(r.status_code != 200):
            raise Exception(r.text)

    def edit(self, guid, data):
        # Because Posting = True does not create records in registers
        if 'Posting' in data:
            raise ValueError('Do not pass the "Posting" field')
        obj = "Document_{}(guid'{}')".format(self.docname, guid)
        url = self.infobase._full_url.format(obj=obj)
        r = requests.patch(url, auth=self.infobase._auth,
                           headers=self.infobase._headers, data=json.dumps(data))
        if(r.status_code != 200):
            raise Exception(r.text)

        # TODO Check whether document changes register records (rePosted)?
        return json.loads(r.text)

    def create(self, data, posting_mode=PostingMode.UNPOST):
        # Because Posting = True does not create records in registers
        if ('Posting' in data) and (data['Posting'] == True):
            raise ValueError('Do not pass the "Posting" field')
        if not 'Date' in data:
            raise ValueError('Date value cannot be an empty date')

        url = self.infobase._full_url.format(obj='Document_' + self.docname)
        r = requests.post(url, auth=self.infobase._auth,
                          headers=self.infobase._headers, data=json.dumps(data))
        if r.status_code != 201:
            raise Exception(r.text)

        new_doc = json.loads(r.text)

        if posting_mode != PostingMode.UNPOST:
            self.post(new_doc['Ref_Key'], posting_mode)

        return new_doc
