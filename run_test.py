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

    # create list of bond dictionaries (test_specs_list) but without metrics, to test metrics correctly calculated
    metrics_columns = ['annual_interest', 'interest_buy_to_sell', 'interest_buy_to_maturity']
    test_specs_list = df.drop(columns=metrics_columns).to_dict('records')

    actual_metrics_list = run.calculate_metrics(test_specs_list,
                                                buy_date_str='2023-10-01', sell_date_str='2024-10-01',
                                                nominal_value=100)
    expected_metrics_list = df.to_dict('records')  # list of bond dictionaries with metrics

    assert actual_metrics_list == expected_metrics_list
