import json

import requests

from odata1c.core import Infobase
from odata1c.utils import make_url_part


class Catalog:
    infobase: Infobase

    def __init__(self, infobase):
        self.infobase = infobase
        
    # def new_catalog(self):
    #     # TODO new_catalog
    #     pass

    # def edit_catalog(self):
    #     # TODO edit_catalog
    #     pass

    # def get_catalog(self):
    #     # TODO get_catalog
    #     pass

    # def get_catalogs(self):
    #     # TODO get_catalogs
    #     pass

    # def InformationRegister_slicelast(self):
    #     # TODO InformationRegister_slicelast
    #     pass

    # def AccountingRegister_balance(self):
    #     # TODO AccountingRegister_balance
    #     pass

    # def AccumulationRegister_balance(self):
    #     # TODO AccumulationRegister_balance
    #     pass