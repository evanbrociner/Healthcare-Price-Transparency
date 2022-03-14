
from doltpy.cli.read import read_pandas_sql
from doltpy.cli import Dolt, DoltException

def hospitals_per_state(state):
    query = '''SELECT state,COUNT(state) AS sum
    FROM hospitals
    GROUP BY state'''
    repo = Dolt('/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

    result = read_pandas_sql(repo, query)
    print(result)


#def hospitals_per_state(state):


def get_average_price():

    query = '''SELECT AVG(price)
    FROM prices
    GROUP BY code,npi_number'''
    repo = Dolt('/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

    result = read_pandas_sql(repo, query)
    print(result)
