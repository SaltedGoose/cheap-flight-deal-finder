import requests

SHEETY_READ_URL = ''#enter sheety api url here

SHEETY_HEADERS = {
    'Authorization' : '',#enter api key here
    'Content-Type' : 'application/json'
}

index = 2

class DataManager:
    def retrieve_data(self):
        response = requests.get(f'{SHEETY_READ_URL}/prices', headers=SHEETY_HEADERS)
        flight_data = response.json()['prices']
        return flight_data

    def fill_iata_codes(self, iata_list):
        global index
        for code in iata_list:
            new_data = {
                'price': {
                    'iataCode' : code
                }
            }
            response = requests.put(f'{SHEETY_READ_URL}/prices/{index}', headers=SHEETY_HEADERS, json=new_data)
            response.raise_for_status()
            index += 1
            print(f'Code added : {code}')
    
    def get_users(self):
        response = requests.get(f'{SHEETY_READ_URL}/users', headers=SHEETY_HEADERS)
        return response.json()['users']


