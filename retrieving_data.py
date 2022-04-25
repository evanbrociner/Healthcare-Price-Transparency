import os
import pandas as pd
import sqlite3

from geopy.geocoders import Nominatim
from doltpy.cli.read import read_pandas_sql
from doltpy.cli import Dolt, DoltException

import geopy.distance

def get_geo(result_df):

    result_df['combined_address'] = result_df[[
        'street_address', 'city', 'state']].values.tolist()

    result_df['latitude'] = 'NA'
    result_df['longitude'] = 'NA'
    result_df['coordinates'] = 'NA'

    for index in range(len(result_df)):
        try:
            geolocator = Nominatim(user_agent="my_user_agent")
            combined_address = ', '.join(
                result_df.loc[index]['combined_address'])
            loc = geolocator.geocode(combined_address)

            if loc is None:
                loc = geolocator.geocode(
                    result_df.loc[index]['city'] + ', ' +
                    result_df.loc[index]['state'])

            if hasattr(loc, 'latitude'):
                # "coordinates": [ longitude, latitude ]
                result_df.loc[index, 'coordinates'] = [
                    loc.longitude, loc.latitude]
                result_df.loc[index, 'longitude'] = loc.longitude
                result_df.loc[index, 'latitude'] = loc.latitude

        except Exception:
            pass

    return result_df


def close_hospital(df):

    for index_i in range(len(df)):
        km_distance = []
        for index_j in range(len(df)):
            try:

                if index_i != index_j:
                    # print(df.loc[index_i, 'latitude'])
                    # print(df.loc[index_j, 'latitude'])

                    loc1 = (df.loc[index_i, 'latitude'],
                            df.loc[index_i, 'longitude'])

                    loc2 = (df.loc[index_j, 'latitude'],
                            df.loc[index_j, 'longitude'])
                    km_distance.append(geopy.distance.geodesic(loc1, loc2).km)
            except Exception:
                # print(df.loc[index_i])
                pass
        df.loc[index_i, 'km_distance'] = min(km_distance)
    df.to_csv('data/hospitals_coordinates.csv')


def hospitals_per_state():

    query = '''SELECT *
    FROM hospitals'''

    repo = Dolt(
        '/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')
    result_df = read_pandas_sql(repo, query)

    result_df = get_geo(result_df)

    result_df = result_df[result_df.longitude != 'NA']
    result_df = result_df[result_df.latitude != 'NA']
    result_df = result_df.reset_index(drop=True)

    result_df = close_hospital(result_df)

    coordinates_only_df = result_df[result_df.columns[result_df.columns.isin(['npi_number',
                                                                   'longitude',
                                                                    'latitude',
                                                                    'zip_code',
                                                                    'city',
                                                                    'state',
                                                                    'name'
                                                                    'km_distance'])]]

    # result_df = result_df[result_df.columns[result_df.columns.isin([
    #                                                                'longitude',
    #                                                                 'latitude',
    #                                                                 'km_distance',
    #
    #                                                             ])]]

    coordinates_only_df.to_csv('data/hospitals_coordinates.csv')


def average_price_per_code():


             # '90834','90832','90837','90846','90847','90832','90834','90837',
             # '90846' ,'90847' ,'90853','99203' ,'99204' ,'99205' ,'99243' , '99244' ,
             # '99385' ,'99386' ,'80048' ,'80053' ,'80055' , '80061' ,'80069' ,'80076' ,
             # '81000' ,'81001','81002' ,'81003','84153', '84154' ,'84443' ,'85025' ,
             # '85027' ,'85610' ,'85730' ,'70450','70553' ,'72110' ,'72148' ,'72193' ,
             # '73721', '74177' , '76700' ,'76805' ,'76830' ,'77065' ,'77066' ,'77067' ,
             # '216''460' ,'470' ,'473' ,'743' ,'19120' ,'29826' ,'29881' ,'42820' ,'43235' ,
             # '43239' ,'45378' ,'45380' ,'45385' ,'45391','47562' ,'49505' ,'55700'  ,
             # '55866' ,'59400' ,'59510' ,'59610' ,'62322' ,'62323' ,'64483' ,'66821' ,
             # '66984' ,'93000' ,'93452' ,'95810','97110')

    query = '''
    SELECT *

     FROM prices

     WHERE code IN ('80048', '80053', '80055', '80061', '80069', '80076',
                            '81000', '81001', '81002', '81003', '84153', '84154', '84443', '85025',
                            '85027', '85610', '85730')

     '''

    repo = Dolt(
        '/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

    result_df = read_pandas_sql(repo, query)
    result_df.to_csv('data/avg_price.csv', sep=',')


def hospital_merged():

    hospitals_df = pd.read_csv('data/hospitals.csv')
    avg_price_df = pd.read_csv('data/avg_price.csv')
    poverty_rates_df = pd.read_csv('data/poverty_rates.csv')

    merged_df = pd.merge(hospitals_df, avg_price_df,
                         how='inner', on='npi_number')
    #
    # merged_df = pd.merge(merged_df, poverty_rates_df,
    #                      how='inner', on=['city', 'state'])
    merged_df.to_csv('data/merged_data.csv', sep=',')


def price_per_hospital_and_insurance():

    query = '''SELECT AVG(price)
    FROM prices
    GROUP BY code,
            npi_number'''
    repo = Dolt(
        '/Users/evan.brociner/Desktop/Job_Hunting_Projects/hospital-price-transparency')

    result = read_pandas_sql(repo, query)
    print(result)

# The Spearman test


if __name__ == "__main__":

    average_price_per_code()

    if not os.path.isfile('data/hospitals_coordinates.csv'):
        hospitals_per_state()

    result_df = pd.read_csv('data/lat-long/hospitals_coordinates.csv')

    result_df =result_df.dropna()
    result_df = result_df.reset_index(drop=True)

    close_hospital(result_df)




    #
    # if not os.path.isfile('data/hospitals.csv'):
    #     hospitals_per_state()
    #
    # if not os.path.isfile('data/avg_price.csv'):
    #
    # if not os.path.isfile('data/merged_data.csv'):
    #     hospital_merged()
