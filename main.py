import requests
from twilio.rest.api.v2010.account import message
from notification_manager import NotificationManager
from flight_search import FlightSearch
from data_manager import DataManager
import datetime as dt
from dateutil.relativedelta import relativedelta

TOMORROW_DATE = (dt.datetime.date(dt.datetime.today()) + dt.timedelta(days=1)).strftime(f'%d/%m/%Y')
SIX_MONTHS_DATE = (dt.datetime.today() + relativedelta(months=+6)).strftime(f'%d/%m/%Y')

data_manager = DataManager()
sheet_data = data_manager.retrieve_data()
flight_searcher = FlightSearch()
list_of_codes = flight_searcher.retrieve_iata_codes(sheet_data)
data_manager.fill_iata_codes(list_of_codes)
sheet_data = data_manager.retrieve_data()
flight_price_list = flight_searcher.flight_search(sheet_data)

for flight in flight_price_list:
    price_to_fly = int(flight.price)
    lowest_price = int(flight.lowest_price)
    destination = flight.destination
    iata_code = str(flight.iata_code)
    notifier = NotificationManager()
    list_of_users = data_manager.get_users()

    if lowest_price > price_to_fly:
        #notifier.send_message(price_to_fly, destination, iata_code)
        message_to_send = f'Subject:Low price alert!\n\nOnly £{price_to_fly} to fly from London-STN to {destination}-{iata_code}, from {flight.out_date} to {flight.return_date}'.encode('utf-8')
        if flight.stop_overs == 1:
            message_to_send += f'\nFlight has {flight.stop_overs} stop over, via {flight.connecting_city}'
        notifier.send_email(message_to_send, list_of_users)
