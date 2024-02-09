import re
from dataclasses import dataclass, field

import requests
from decouple import config


@dataclass()
class AddressService:

    api_host: str = field(default=config('ADDRESS_API_HOST'))
    api_username: str = field(default=config('ADDRESS_API_KEY'))

    def get_params(self, service, search_param):
        params = [('username', self.api_username), ('lang', 'pt')]
        if service == 'postalCodeSearch':
            params.append(('postalcode', search_param))
        elif service == 'children':
            params.append(('geonameId', search_param))
            params.append(('hierarchy', 'geography'))
        return params

    def make_request(self, service, search_param, key):
        params = self.get_params(service, search_param)
        try:
            resp = requests.get(
                f'{self.api_host}/{service}',
                params=params,
                headers={'Accept': 'application/json'},
            )
            result = resp.json()[key]
        except Exception as error:
            raise ImportError(error)
        return result

    def list_address_by_postalcode(self, postalcode):
        api_service = 'postalCodeSearch'
        to_output = {}
        results = self.make_request(
            service=api_service, search_param=postalcode, key='postalCodes'
        )
        if results:
            to_output['uf'] = results[0]['adminName1'].strip()
            to_output['country'] = AddressService().get_country_by_code(
                results[0]['countryCode']
            )
            to_output['city'] = results[0]['placeName']
            return to_output
        return None

    def split_uk_region(self):
        uk_subdivision = AddressService().list_ufs_in_country('Reino Unido')[0]
        for division in uk_subdivision:
            division['countryName'] = division['name']
        return uk_subdivision

    def list_all_countries(self):
        api_service = 'countryInfoJSON'
        return self.make_request(service=api_service, search_param=None, key='geonames')

    def retrieve_obj_in_list(self, obj, list, key):
        return [
            element
            for element in list
            if re.search(str.lower(obj), str.lower(element[key]))
        ]

    def get_country_by_name(self, country):
        country, index = self.treat_country_input(country)
        country_list = self.list_all_countries()
        return self.retrieve_obj_in_list(country, country_list, key='countryName')

    def get_country_by_code(self, country_code):
        country_list = self.list_all_countries()
        country = self.retrieve_obj_in_list(country_code, country_list, key='countryCode')
        return country[0]['countryName']

    def treat_country_input(self, country_name):
        index = 0
        if re.search('estados unidos', str.lower(country_name)) or re.search(
            'estados', str.lower(country_name)
        ):
            country_name = 'EUA'
            index = 1
        return [country_name, index]

    def get_uf_by_name(self, uf, country_name):
        country, index = self.treat_country_input(country_name)
        uf_list = self.list_ufs_in_country(country)[0]
        if uf_list:
            return self.retrieve_obj_in_list(uf, uf_list, 'name')
        return None

    def is_uk_region(self, country_name):
        if country_name in ('Inglaterra', 'Gales', 'Escócia', 'Northern Ireland'):
            return True
        return False

    def list_ufs_in_country(self, country_name):
        api_service = 'children'
        is_uk_region = self.is_uk_region(country_name)
        country_name, country_index = self.treat_country_input(country_name)

        if country_name == 'EUA':
            country_index = 1

        country_list = (
            self.split_uk_region()
            if is_uk_region
            else self.get_country_by_name(country_name)
        )

        country_id = [
            self.retrieve_obj_in_list(country_name, country_list, key='countryName')[
                country_index
            ]['geonameId']
        ]

        ufs_collection = []
        if country_id:
            for id_country in country_id:
                results = self.make_request(
                    service=api_service, search_param=id_country, key='geonames'
                )
                if is_uk_region:
                    for result in results:
                        result['countryName'] = result['adminName1']
                ufs_collection.append(results)
            return ufs_collection
        return None

    def list_cities_in_uf(self, uf):
        api_service = 'children'
        return self.make_request(service=api_service, search_param=uf, key='geonames')
