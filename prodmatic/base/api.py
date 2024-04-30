from restcountries.api import RestCountriesAPI
from abc import ABC, abstractmethod


class StoreAPI(ABC):
    countries_api = RestCountriesAPI()

    def __init__(self):
        pass

    @abstractmethod
    def iap_exists(self, iap_identifier):
        pass

    @abstractmethod
    def add_iap(self, iap_identifier, iap_data):
        pass

    @abstractmethod
    def update_iap(self, iap_identifier, iap_data):
        pass

    @abstractmethod
    def get_iap(self, iap_identifier):
        pass

    @abstractmethod
    def subscription_exists(self, subscription_identifier):
        pass

    @abstractmethod
    def add_subscription(self, subscription_identifier, subscription_data):
        pass

    @abstractmethod
    def update_subscription(self, subscription_identifier, subscription_data):
        pass

    @abstractmethod
    def get_subscription(self, subscription_identifier):
        pass
