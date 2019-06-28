from odata1cw.core import Infobase
from odata1cw.postingmode import PostingMode
from datetime import datetime
from odata1cw.document import Document
from odata1cw.catalog import Catalog
from odata1cw.informationregister import InformationRegister


# example doc query,
connection = Infobase('http://localhost/', 'Infobase1', 'User', '123')
cpl = Document(connection, 'Пользователи')
users = cpl.query(top=3)
print(users)

# example slice last 
inforeg = InformationRegister(connection, 'OdometerReadings')
period_value = f"Period = datetime'{datetime.now().isoformat()}'"
guid='b4199e50-4510-11e9-90ec-00155d580419'
condition_value=f"Condition='Auto_Key eq guid'{guid}''"
res = inforeg.slice_last(
    period=period_value,condition=condition_value,select="Reading", orderby="Reading desc",expand='Auto',)
print(res)
