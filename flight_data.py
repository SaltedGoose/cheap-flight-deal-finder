class FlightData:
    def __init__(self, destination, iata_code, price, lowest_price, out_date, return_date, stop_overs = 0, connecting_city=''):
        self.destination = destination
        self.iata_code = iata_code
        self.price = price
        self.lowest_price = lowest_price
        self.out_date = out_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        self.connecting_city = connecting_city