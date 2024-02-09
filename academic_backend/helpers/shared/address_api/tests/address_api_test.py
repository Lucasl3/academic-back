import django
import pytest
from rest_framework.test import APIClient

django.setup()


class TestAddressAPi:

    BASE_URL = '/api/v1/address'

    @pytest.fixture
    def client(self) -> APIClient:
        return APIClient()

    def test_if_retrieve_all_countries(self, client):
        response = client.get(f'{self.BASE_URL}/countries')
        assert response.status_code == 200

    def test_if_retrieve_postalcode(self, client):
        response_200 = client.get(
            f'{self.BASE_URL}/postalcode', **{'QUERY_STRING': 'postalcode=57460000'}
        )

        response_404_not_provided = client.get(
            f'{self.BASE_URL}/postalcode', **{'QUERY_STRING': 'postalcode='}
        )

        response_404_not_found = client.get(
            f'{self.BASE_URL}/postalcode', **{'QUERY_STRING': 'postalcode=asasas'}
        )

        assert response_200.status_code == 200
        assert response_404_not_provided.status_code == 404
        assert response_404_not_found.status_code == 404
        assert response_200.json()['country'] == 'Brasil'
        assert response_200.json()['uf'] == 'Alagoas'
        assert response_200.json()['city'] == 'Piranhas'

    def test_if_retrieve_ufs(self, client):
        response_200 = client.get(
            f'{self.BASE_URL}/ufs', **{'QUERY_STRING': 'country=Brasil'}
        )

        response_200_to_england_input = client.get(
            f'{self.BASE_URL}/ufs', **{'QUERY_STRING': 'country=Inglaterra'}
        )

        response_200_to_united_states_input = client.get(
            f'{self.BASE_URL}/ufs', **{'QUERY_STRING': 'country=Estados Unidos'}
        )

        response_404_not_provided = client.get(
            f'{self.BASE_URL}/ufs', **{'QUERY_STRING': 'country='}
        )
        response_404_not_found = client.get(
            f'{self.BASE_URL}/ufs', **{'QUERY_STRING': 'country=Marte'}
        )

        response_uf_list_brasil = response_200.json()[0]
        response_uf_in_brasilian_state = [
            element for element in response_uf_list_brasil if element['name'] == 'Alagoas'
        ][0]

        assert response_200.status_code == 200
        assert response_200_to_england_input.status_code == 200
        assert response_200_to_united_states_input.status_code == 200
        assert response_404_not_provided.status_code == 404
        assert response_404_not_found.status_code == 404
        assert response_uf_in_brasilian_state['name'] == 'Alagoas'

    def test_if_retrieve_cities(self, client):
        response_200 = client.get(
            f'{self.BASE_URL}/cities', **{'QUERY_STRING': 'country=Brasil&uf=Alagoas'}
        )

        response_200_to_england_input = client.get(
            f'{self.BASE_URL}/cities',
            **{'QUERY_STRING': 'country=Inglaterra&uf=Manchester'},
        )

        response_200_to_united_states_input = client.get(
            f'{self.BASE_URL}/cities',
            **{'QUERY_STRING': 'country=Estados Unidos&uf=Alabama'},
        )

        response_404_not_provided = client.get(
            f'{self.BASE_URL}/cities', **{'QUERY_STRING': 'country='}
        )

        response_404_not_found = client.get(
            f'{self.BASE_URL}/cities', **{'QUERY_STRING': 'country=Marte'}
        )

        response_city_in_uf_list_brasil = response_200.json()
        response_city_in_uf_in_brasilian_alagoas_state = [
            element
            for element in response_city_in_uf_list_brasil
            if element['name'] == 'Maceió'
        ][0]

        assert response_200.status_code == 200
        assert response_200_to_england_input.status_code == 200
        assert response_200_to_united_states_input.status_code == 200
        assert response_404_not_provided.status_code == 404
        assert response_404_not_found.status_code == 404
        assert response_city_in_uf_in_brasilian_alagoas_state['name'] == 'Maceió'
