from restcountries.api import RestCountriesAPI
from pppfy.converter import Converter
from moneymatters.api import ExchangeAPI, Formatter
from abc import ABC, abstractmethod


class StorePricing(ABC):
    countries_api = RestCountriesAPI()
    pppfy_converter = Converter()
    forex_api = ExchangeAPI()
    formatter = Formatter()

    def __init__(self):
        # A map of iso2_code: 3 letter ISO code for the currency used for that country in playstore
        self.map_country_to_store_currency = {}

        # A map of iso2_code: price
        self.map_country_to_reference_rounded_price = {}

    @abstractmethod
    def fetch_country_to_store_currency_map(self, store_reference_prices_file):
        """
        Get the recent most information on the currency that a given store supports for a given country
        """
        pass

    @abstractmethod
    def load_country_to_reference_rounded_prices(self):
        """
        Load, from local/network, reference prices for all the countries supported in a given store
        """
        pass

    def get_store_price_mapping(self, source_country="US", source_price=79, destination_country=None, year=None):
        ppp_price_mapping = self.pppfy_converter.get_price_mapping(
            source_country, source_price, destination_country, year
        )

        if isinstance(ppp_price_mapping, dict):
            ppp_price_mapping = [ppp_price_mapping]

        store_prices = []
        for mapping in ppp_price_mapping:
            iso2_code = mapping["ISO2"]
            local_price = mapping["ppp_adjusted_local_price"]
            # local_currency = mapping["local_currency"]

            # Is the country featured in appstore list of countries?
            if iso2_code not in self.map_country_to_reference_rounded_price:
                continue

            appstore_currency, appstore_price = self.forex_api.convert(iso2_code, local_price, local_currency)

            # Some heavily devalued currencies might end up with very low usd values < 10
            # TODO needs a better fix
            if appstore_price < 10:
                appstore_price = 10

            rounded_price = self.formatter.apply_price_format(price=appstore_price, format=x)

            mapping["appstore_currency"] = appstore_currency
            mapping["appstore_price"] = rounded_price
            store_prices.append(mapping)

        return store_prices
