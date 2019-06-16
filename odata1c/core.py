import json

import requests

from odata1c.postingmode import PostingMode


class InfoBase:
    server: str
    infobase: str
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
        self._auth = requests.auth.HTTPBasicAuth(username, password)

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
            raise Exception(r.text)
        return json.loads(r.text)['value']

    # TODO documents $count
    # TODO documents $inlinecount
    # TODO documents $orderby
    # TODO documents $expand

    def get_document(self, name, guid, select=None):
        obj = "Document_{}(guid'{}')".format(name, guid)
        url = self._full_url.format(obj=obj)
        _url_select = self._make_url_part('select', select, str)
        url = url + _url_select
        r = requests.get(url, auth=self._auth, headers=self._headers)
        if(r.status_code != 200):
            raise Exception(r.text)
        return json.loads(r.text)

    def post_document(self, name, guid, posting_mode):
        obj = "Document_{}(guid'{}')/Post".format(name, guid)
        url = self._full_url.format(obj=obj)
        if posting_mode == PostingMode.OPER:
            url = url + '&PostingModeOperational=false'
        elif posting_mode == PostingMode.POST:
            url = url + '&PostingModeOperational=true'
        else:
            raise ValueError('Use unpost_document() for unposting')
        r = requests.post(url, auth=self._auth, headers=self._headers)
        if(r.status_code != 200):
            raise Exception(r.text)

    def unpost_document(self, name, data):
        # TODO unpost_document
        pass

    # TODO Check whether document changes register records (rePosted)?
    def edit_document(self, name, guid, data):
        # Because Posting = True does not create records in registers
        if 'Posting' in data:
            raise ValueError('Do not pass the "Posting" field')
        obj = "Document_{}(guid'{}')".format(name, guid)
        url = self._full_url.format(obj=obj)
        r = requests.patch(url, auth=self._auth,
                           headers=self._headers, data=json.dumps(data))
        if(r.status_code != 200):
            raise Exception(r.text)

        return json.loads(r.text)

    def new_document(self, name, data, posting_mode=PostingMode.UNPOST):
        # Because Posting = True does not create records in registers
        if ('Posting' in data) and (data['Posting'] == True):
            raise ValueError('Do not pass the "Posting" field')
        if not 'Date' in data:
            raise ValueError('Date value cannot be an empty date')

        url = self._full_url.format(obj='Document_' + name)
        r = requests.post(url, auth=self._auth,
                          headers=self._headers, data=json.dumps(data))
        if r.status_code != 201:
            raise Exception(r.text)

        new_doc = json.loads(r.text)

        if posting_mode != PostingMode.UNPOST:
            self.post_document(name, new_doc['Ref_Key'], posting_mode)

        return new_doc
