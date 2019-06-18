from odata1cw.core import Infobase
from odata1cw.postingmode import PostingMode
from datetime import datetime
from odata1cw.document import Document
from odata1cw.catalog import Catalog

connection = Infobase('http://localhost/','Infobase1','User','123')
cpl = Document(connection, 'Пользователи')
users = cpl.query(top=3)
print(users)
