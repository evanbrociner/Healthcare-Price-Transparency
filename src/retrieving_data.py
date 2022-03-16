
from doltpy.cli.read import read_pandas_sql
from doltpy.cli import Dolt, DoltException

import os

def hospitals_per_state():
    query = '''SELECT state,COUNT(state) AS sum
    FROM hospitals
    GROUP BY state'''
    repo = Dolt(
        '/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')
    result_df = read_pandas_sql(repo, query)
    result_df.to_csv('data/hospitals_per_state.csv', sep=',')


def average_price_per_code():

    query = '''SELECT code,price
     FROM prices'''

    repo = Dolt(
        '/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

    result_df = read_pandas_sql(repo, query)

    result_df.to_csv('data/avg_price.csv', sep=',')

def price_per_hospital():

    query = '''SELECT npi_number,code, AVG(price)
    FROM prices
    GROUP BY code,
             npi_number'''
    repo = Dolt(
        '/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

    result_df = read_pandas_sql(repo, query)
    result_df.to_csv('data/price_per_hospital.csv', sep=',')


def price_per_hospital_and_insurance():

    query = '''SELECT AVG(price)
    FROM prices
    GROUP BY code,
            npi_number'''
    repo = Dolt(
        '/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

    result = read_pandas_sql(repo, query)
    print(result)



if __name__ == "__main__":

    if not os.path.isfile('data/avg_price.csv'):
        average_price_per_code()

    if not os.path.isfile('data/hospitals_per_state.csv'):
        hospitals_per_state()

    if not os.path.isfile('data/price_per_hospital.csv'):
        price_per_hospital()
