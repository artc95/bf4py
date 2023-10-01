import pytest
import run


def test_list_key_specs():
    isin_list = ['XS1218821756', 'XS1637276848']
    actual_specs_list = run.list_key_specs(isin_list)

    expected_specs_list = [
        {'ISIN': 'XS1218821756', 'issuer': 'ABN AMRO Bank N.V.', 'coupon_%': 1.0, 'last_price': 95.16, 'maturity_date': '2025-04-16', 'website_url': 'https://www.boerse-frankfurt.de/bond/XS1218821756'}, # noqa
        {'ISIN': 'XS1637276848', 'issuer': 'Zypern, Republik', 'coupon_%': 2.75, 'last_price': 99.143, 'maturity_date': '2024-06-27', 'website_url': 'https://www.boerse-frankfurt.de/bond/XS1637276848'}  # noqa
    ]
    assert actual_specs_list == expected_specs_list
