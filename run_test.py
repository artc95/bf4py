from datetime import datetime
import pandas as pd
import run


def test_list_key_specs():
    isin_list = ['XS1218821756', 'XS1637276848']
    actual_specs_list = run.list_key_specs(isin_list)

    expected_specs_list = [
        {'ISIN': 'XS1218821756', 'issuer': 'ABN AMRO Bank N.V.', 'coupon_%': 1.0, 'last_price': 95.16, 'maturity_date': '2025-04-16', 'website_url': 'https://www.boerse-frankfurt.de/bond/XS1218821756'}, # noqa
        {'ISIN': 'XS1637276848', 'issuer': 'Zypern, Republik', 'coupon_%': 2.75, 'last_price': 99.143, 'maturity_date': '2024-06-27', 'website_url': 'https://www.boerse-frankfurt.de/bond/XS1637276848'}  # noqa
    ]
    assert actual_specs_list == expected_specs_list

# TO RUN: pytest -s run_test.py::test_calculate_metrics ('-s' flag, and fail the test to display logging)
def test_calculate_metrics():
    df = pd.read_csv('run_test.csv')
    specs_list_of_dicts = df.to_dict('records')

    actual_metrics_list = run.calculate_metrics(specs_list_of_dicts, '2024-10-01')
    expected_metrics_list = ['2024-10-01', '2024-10-01', datetime(2024, 3, 31)]

    assert actual_metrics_list == expected_metrics_list
