
from doltpy.cli.read import read_pandas_sql
from doltpy.cli import Dolt, DoltException


query = '''SELECT state,COUNT(state) AS sum
FROM hospitals
GROUP BY state'''
repo = Dolt('/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

result = read_pandas_sql(repo, query)
print(result)
#
#
# tables = doltpy.dolt.ls()
