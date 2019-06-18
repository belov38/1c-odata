# 1c-odata
1C v8 OData wrapper

```python
from odata1cw.core import Infobase
from odata1cw.postingmode import PostingMode
from datetime import datetime
from odata1cw.document import Document
from odata1cw.catalog import Catalog

connection = Infobase('http://myserver:port/','Infobase1','User','Password')

users = Catalog(connection,'Пользователи')
user.query() # get all
user.query(top=5)
user.query(top=5, skip=2)
user.query(select='Description, DeletionMark')

# Use singl quotes for strings!
f = "(Description eq 'IvanPetrov') and (DeletionMark eq false)"
user.query(odata_filter=f)

new = {'Description':'Новый пользователь','Комментарий':'hello odata'}

new_user = user.create(new)
edit_data = {'Комментарий':'hello odata edit'}
user.edit(guid=new_user['Ref_Key'], data=edit_data)
```
