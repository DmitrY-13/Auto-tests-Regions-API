import math
from http import HTTPStatus

import pytest

from api.client import ApiClient
from api.responses import RegionsError, RegionsResponse
from test_data.regions import RegionsErrorMessages, RegionsTestData


class TestQQuery:
    @pytest.mark.parametrize(
        'q',
        RegionsTestData.Q_STRINGS,
        ids=RegionsTestData.Q_STRINGS_IDS,
    )
    def test_get_regions_with_q(self, client: ApiClient, q):
        regions_response = client.get_regions(q=q)
        assert regions_response.status_code == HTTPStatus.OK

        regions_json = RegionsResponse.model_validate(regions_response.json())
        for item in regions_json.items:
            assert q.lower() in item.name.lower()

    @pytest.mark.parametrize(
        'q',
        RegionsTestData.Q_STRINGS,
        ids=RegionsTestData.Q_STRINGS_IDS,
    )
    @pytest.mark.parametrize(
        'page_number',
        (2, 0),
        ids=('valid page number', 'invalid page number'),
    )
    def test_get_regions_with_q_and_page_number(self, client: ApiClient, q, page_number):
        regions_response1 = client.get_regions(q=q)
        regions_response2 = client.get_regions(q=q, page=page_number)

        assert regions_response1.status_code == HTTPStatus.OK
        assert regions_response2.status_code == HTTPStatus.OK

        regions_json1 = RegionsResponse.model_validate(regions_response1.json())
        assert regions_json1.total == RegionsTestData.TOTAL_ITEMS
        regions_json2 = RegionsResponse.model_validate(regions_response2.json())
        assert regions_json2.total == RegionsTestData.TOTAL_ITEMS

        assert regions_json1 == regions_json2

    @pytest.mark.parametrize(
        'q',
        RegionsTestData.Q_STRINGS,
        ids=RegionsTestData.Q_STRINGS_IDS,
    )
    @pytest.mark.parametrize(
        'page_size',
        (5, 3),
        ids=('valid page size', 'invalid page size'),
    )
    def test_get_regions_with_q_and_page_size(self, client: ApiClient, q, page_size):
        regions_response1 = client.get_regions(q=q)
        regions_response2 = client.get_regions(q=q, page_size=page_size)

        assert regions_response1.status_code == HTTPStatus.OK
        assert regions_response2.status_code == HTTPStatus.OK

        regions_json1 = RegionsResponse.model_validate(regions_response1.json())
        assert regions_json1.total == RegionsTestData.TOTAL_ITEMS
        regions_json2 = RegionsResponse.model_validate(regions_response2.json())
        assert regions_json2.total == RegionsTestData.TOTAL_ITEMS

        assert regions_json1 == regions_json2

    @pytest.mark.parametrize(
        'q',
        RegionsTestData.Q_STRINGS,
        ids=RegionsTestData.Q_STRINGS_IDS,
    )
    @pytest.mark.parametrize(
        'country_code',
        ('cz', 'yz'),
        ids=('valid country code', 'invalid country code'),
    )
    def test_get_regions_with_q_and_country_code(self, client: ApiClient, q, country_code):
        regions_response1 = client.get_regions(q=q)
        regions_response2 = client.get_regions(q=q, country_code=country_code)

        assert regions_response1.status_code == HTTPStatus.OK
        assert regions_response2.status_code == HTTPStatus.OK

        regions_json1 = RegionsResponse.model_validate(regions_response1.json())
        assert regions_json1.total == RegionsTestData.TOTAL_ITEMS
        regions_json2 = RegionsResponse.model_validate(regions_response2.json())
        assert regions_json2.total == RegionsTestData.TOTAL_ITEMS

        assert regions_json1 == regions_json2

    @pytest.mark.parametrize('q', ('1', '12'))
    def test_get_regions_with_q_value_length_less_than_3_symbols(self, client: ApiClient, q):
        regions_response = client.get_regions(q=q)
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())
        assert (
            regions_error.error.message == RegionsErrorMessages.Q_VALUE_LENGTH_LESS_THAN_3_SYMBOLS
        )

    def test_get_regions_with_q_value_length_greater_than_30_symbols(self, client: ApiClient):
        regions_response = client.get_regions(q='a' * 31)
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())
        assert (
            regions_error.error.message
            == RegionsErrorMessages.Q_VALUE_LENGTH_GRATER_THAN_30_SYMBOLS
        )


class TestCountryCodeQuery:
    @pytest.mark.parametrize(
        'country_code',
        RegionsTestData.ACCEPTABLE_COUNTRY_CODES,
    )
    def test_get_regions_with_acceptable_country_code(self, client: ApiClient, country_code):
        page_number = 1

        while True:
            regions_response = client.get_regions(page=page_number, country_code=country_code)
            assert regions_response.status_code == HTTPStatus.OK

            regions_json = RegionsResponse.model_validate(regions_response.json())
            assert regions_json.total == RegionsTestData.TOTAL_ITEMS

            if len(regions_json.items) == 0:
                break

            for item in regions_json.items:
                assert item.country.code == country_code

            page_number += 1

    @pytest.mark.parametrize(
        'country_code',
        RegionsTestData.ACCEPTABLE_COUNTRY_CODES,
    )
    def test_get_regions_with_acceptable_country_code_and_switching_pages(
        self, client: ApiClient, country_code
    ):
        page_number = 1

        while True:
            regions_response1 = client.get_regions(page=page_number, country_code=country_code)
            regions_response2 = client.get_regions(page=page_number + 1, country_code=country_code)

            assert regions_response1.status_code == HTTPStatus.OK
            assert regions_response2.status_code == HTTPStatus.OK

            regions_json1 = RegionsResponse.model_validate(regions_response1.json())
            assert regions_json1.total == RegionsTestData.TOTAL_ITEMS
            regions_json2 = RegionsResponse.model_validate(regions_response2.json())
            assert regions_json2.total == RegionsTestData.TOTAL_ITEMS

            if len(regions_json2.items) == 0:
                break

            assert regions_json1 != regions_json2

            page_number += 1

    @pytest.mark.parametrize(
        'country_code',
        RegionsTestData.UNACCEPTABLE_COUNTRY_CODES,
    )
    def test_get_regions_with_unacceptable_country_code(self, client: ApiClient, country_code):
        regions_response = client.get_regions(country_code=country_code)
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())
        assert regions_error.error.message == RegionsErrorMessages.UNACCEPTABLE_COUNTRY_CODE

    def test_get_regions_with_non_existing_country_code(self, client: ApiClient):
        regions_response = client.get_regions(country_code='yz')
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())
        assert regions_error.error.message == RegionsErrorMessages.UNACCEPTABLE_COUNTRY_CODE

    def test_get_regions_with_empty_country_code(self, client: ApiClient):
        regions_response = client.get_regions(country_code='')
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())
        assert regions_error.error.message == RegionsErrorMessages.UNACCEPTABLE_COUNTRY_CODE


class TestPageQuery:
    @pytest.mark.parametrize(
        'page_size',
        RegionsTestData.ACCEPTABLE_PAGES_SIZES,
    )
    def test_get_regions_empty_list_page(self, client: ApiClient, page_size):
        page = math.ceil(RegionsTestData.TOTAL_ITEMS / page_size) + 1

        regions_response = client.get_regions(page=page, page_size=page_size)
        assert regions_response.status_code == HTTPStatus.OK

        regions_json = RegionsResponse.model_validate(regions_response.json())
        assert regions_json.total == RegionsTestData.TOTAL_ITEMS
        assert len(regions_json.items) == 0

    def test_get_regions_default_page(self, client: ApiClient):
        regions_response1 = client.get_regions()
        regions_response2 = client.get_regions(page=RegionsTestData.DEFAULT_PAGE_NUMBER)

        assert regions_response1.status_code == HTTPStatus.OK
        assert regions_response2.status_code == HTTPStatus.OK

        regions_json1 = RegionsResponse.model_validate(regions_response1.json())
        assert regions_json1.total == RegionsTestData.TOTAL_ITEMS
        regions_json2 = RegionsResponse.model_validate(regions_response2.json())
        assert regions_json2.total == RegionsTestData.TOTAL_ITEMS

        assert regions_json1.items == regions_json2.items

    def test_unique_items_on_pages(self, client: ApiClient):
        page_number = 1

        while True:
            regions_response1 = client.get_regions(page=page_number)
            regions_response2 = client.get_regions(page=page_number + 1)

            assert regions_response1.status_code == HTTPStatus.OK
            assert regions_response2.status_code == HTTPStatus.OK

            regions_json1 = RegionsResponse.model_validate(regions_response1.json())
            assert regions_json1.total == RegionsTestData.TOTAL_ITEMS
            regions_json2 = RegionsResponse.model_validate(regions_response2.json())
            assert regions_json2.total == RegionsTestData.TOTAL_ITEMS

            if len(regions_json2.items) == 0:
                break

            for item1 in regions_json1.items:
                for item2 in regions_json2.items:
                    assert item1 != item2

            page_number += 1

    @pytest.mark.parametrize(
        'page_number',
        RegionsTestData.NON_INTEGERS_VALUES,
        ids=RegionsTestData.NON_INTEGERS_VALUES_IDS,
    )
    def test_get_regions_with_non_integer_page_number(self, client: ApiClient, page_number):
        regions_response = client.get_regions(page=page_number)
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())

        assert regions_error.error.message == RegionsErrorMessages.NON_INTEGER_PAGE_NUMBER

    @pytest.mark.parametrize(
        'page_number',
        RegionsTestData.UNACCEPTABLE_PAGE_NUMBERS,
    )
    def test_get_regions_with_unacceptable_page_number(self, client: ApiClient, page_number):
        regions_response = client.get_regions(page=page_number)
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())

        assert regions_error.error.message == RegionsErrorMessages.PAGE_NUMBER_LESS_THAN_1


class TestPageSizeQuery:
    def test_get_default_page(self, client: ApiClient):
        regions_response = client.get_regions()
        assert regions_response.status_code == HTTPStatus.OK

        regions_json = RegionsResponse.model_validate(regions_response.json())
        assert regions_json.total == RegionsTestData.TOTAL_ITEMS
        assert len(regions_json.items) == RegionsTestData.DEFAULT_PAGE_SIZE

    @pytest.mark.parametrize(
        'page_size',
        RegionsTestData.ACCEPTABLE_PAGES_SIZES,
    )
    def test_get_pages_with_acceptable_page_sizes(self, client: ApiClient, page_size):
        regions_response = client.get_regions(page_size=page_size)
        assert regions_response.status_code == HTTPStatus.OK

        regions_json = RegionsResponse.model_validate(regions_response.json())
        assert regions_json.total == RegionsTestData.TOTAL_ITEMS
        assert len(regions_json.items) == page_size

    @pytest.mark.parametrize(
        'page_size',
        RegionsTestData.UNACCEPTABLE_PAGES_SIZES,
    )
    def test_get_pages_with_unacceptable_page_sizes(self, client: ApiClient, page_size):
        regions_response = client.get_regions(page_size=page_size)
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_json = RegionsError.model_validate(regions_response.json())
        assert regions_json.error.message == RegionsErrorMessages.UNACCEPTABLE_PAGE_SIZE

    @pytest.mark.parametrize(
        'page_size',
        RegionsTestData.NON_INTEGERS_VALUES,
        ids=RegionsTestData.NON_INTEGERS_VALUES_IDS,
    )
    def test_get_regions_with_non_integer_page_size(self, client: ApiClient, page_size):
        regions_response = client.get_regions(page_size=page_size)
        assert regions_response.status_code == HTTPStatus.BAD_REQUEST

        regions_error = RegionsError.model_validate(regions_response.json())

        assert regions_error.error.message == RegionsErrorMessages.NON_INTEGER_PAGE_SIZE

    @pytest.mark.parametrize(
        ('page_size1', 'page_size2'),
        (
            (5, 10),
            (10, 15),
            (15, None),
        ),
        ids=(
            '5 and 10',
            '10 and 15',
            '15 and default',
        ),
    )
    def test_same_items_order(self, client: ApiClient, page_size1, page_size2):
        regions_response1 = client.get_regions(page_size=page_size1)
        regions_response2 = client.get_regions(page_size=page_size2)

        assert regions_response1.status_code == HTTPStatus.OK
        assert regions_response2.status_code == HTTPStatus.OK

        regions_json1 = RegionsResponse.model_validate(regions_response1.json())
        assert regions_json1.total == RegionsTestData.TOTAL_ITEMS
        regions_json2 = RegionsResponse.model_validate(regions_response2.json())
        assert regions_json2.total == RegionsTestData.TOTAL_ITEMS

        for item1, item2 in zip(regions_json1.items, regions_json2.items):
            assert item1 == item2
