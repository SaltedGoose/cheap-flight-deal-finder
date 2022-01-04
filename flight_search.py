import requests
from requests.models import Response
from flight_data import FlightData
from data_manager import DataManager
import datetime as dt
from dateutil.relativedelta import relativedelta

LONDON_CODE = 'STN'
TOMORROW_DATE = (dt.datetime.date(dt.datetime.today()) + dt.timedelta(days=1)).strftime(f'%d/%m/%Y')
SIX_MONTHS_DATE = (dt.datetime.today() + relativedelta(months=+6)).strftime(f'%d/%m/%Y')

FLIGHT_SEARCH_API_KEY = '' #enter tequila api key here
FLIGHT_CODE_SEARCH_ENDPOINT = ''#enter flight code search endpoint here
FLIGHT_SEARCH_ENDPOINT = ''#enter flight search endpoint here

FLIGHT_SEARCH_HEADERS = {
    'apikey' : FLIGHT_SEARCH_API_KEY
}

class FlightSearch:
    def retrieve_iata_codes(self, sheet_data):
        list_of_codes = []
        for data in sheet_data:
            query = {"term": data['city'], "location_types": "city"}
            response = requests.get(url=f'{FLIGHT_CODE_SEARCH_ENDPOINT}/query', headers=FLIGHT_SEARCH_HEADERS, params=query)
            code = response.json()["locations"][0]['code']
            list_of_codes.append(code)
        return list_of_codes


    def flight_search(self, sheet_data) -> list:
        price_list = []
        for flight in sheet_data:
            print(flight['iataCode'])
            flight_search_params = {
                'fly_from' : LONDON_CODE,
                'fly_to' : flight['iataCode'],
                'date_from' : TOMORROW_DATE,
                'date_to' : SIX_MONTHS_DATE,
                "nights_in_dst_from": 7,
                "nights_in_dst_to": 28,
                "flight_type": "round",
                "one_for_city": 1,
                "max_stopovers": 0,
                "curr": "GBP"
            }
            response = requests.get(f'{FLIGHT_SEARCH_ENDPOINT}', headers=FLIGHT_SEARCH_HEADERS, params=flight_search_params)
            response.raise_for_status()
            try:
                data = response.json()['data'][0]
            except IndexError:
                flight_search_params['max_stopovers'] = 1
                response = requests.get(f'{FLIGHT_SEARCH_ENDPOINT}', headers=FLIGHT_SEARCH_HEADERS, params=flight_search_params)
                response.raise_for_status()
                try:
                    data = response.json()['data'][0]
                except IndexError:
                    print('Flight unavaliable')
                else:
                    price_list.append(FlightData(
                        destination = data['cityTo'], 
                        iata_code = data['cityCodeTo'], 
                        price = data['price'], 
                        lowest_price = flight['lowestPrice'], 
                        out_date = data['route'][0]['local_departure'].split('T')[0],
                        return_date = data['route'][2]['local_departure'].split('T')[0],
                        stop_overs = 1,
                        connecting_city = data['route'][0]['cityTo']
                        )
                    )
            else:
                price_list.append(FlightData(
                    destination = data['cityTo'], 
                    iata_code = data['cityCodeTo'], 
                    price = data['price'], 
                    lowest_price = flight['lowestPrice'], 
                    out_date = data['route'][0]['local_departure'].split('T')[0],
                    return_date = data['route'][1]['local_departure'].split('T')[0]
                    )
                )
                print('Flight avaliable')

        return price_list

