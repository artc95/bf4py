from bf4py import BF4Py
import csv
from datetime import datetime
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s Local >>> %(message)s',
                    datefmt='%Y%m%d %H:%M:%S')


def main(degiro_csv: str, output_name: str, sell_date_str: str):
    """
    TODO: calculate profit based on price, coupon and maturity e.g. AT0000383864
    TODO: from a selection of bonds with their specifics, input an end date, calculate bond with highest profit?
    TODO: get company details - industry, latest news
    """
    isin_list = extract_csv_isin(degiro_csv)
    specs_list = list_key_specs(isin_list)
    metrics_list = calculate_metrics(specs_list, sell_date_str)
    csv_key_specs(specs_list, output_name)


def extract_csv_isin(filename: str):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        isin_list = []
        for row in csv_reader:
            if row[0] != 'KV':  # rows without 'KV' as first element, only contain bond name as first element
                continue

            isin = row[1][-12:]  # some values in 'ISIN' column have more than ISIN, e.g. 'OETM | AT0000A0DXC2'
            isin_list.append(isin)

    logging.info(f'run.extract_csv_isin - last isin in isin_list is {isin_list[-1]}')
    return isin_list


def list_key_specs(isin_list: list):
    bf4py = BF4Py(default_isin='XS0968913342', default_mic='XFRA')
    logging.info('run.list_key_specs - class object bf4py initialized')
    specs_list = []
    for isin in isin_list:
        try:
            data = get_bond_data(bf4py, isin)
            specs = extract_key_specs(data)
            specs_list.append(specs)
        except Exception as e:
            logging.info(f'run.list_key_specs - exception {e}')

    logging.info(f'run.list_key_specs - last item is {specs_list[-1]}')
    return specs_list


def get_bond_data(bf4py, isin: str):
    instrument_data = bf4py.bonds.bond_data(isin=isin)
    """sample dict of data:
        {'isin': 'IE00B6X95T99', 
        'type': {'originalValue': '220', 'translations': {'de': 'Währungsanleihen', 'en': 'Currency bonds'}}, 
        'market': {'originalValue': 'OPEN', 'translations': {'de':'Freiverkehr', 'en': 'Open Market'}}, 
        'subSegment': None, 'cupon': 3.4, 'interestPaymentPeriod': None, 'firstAnnualPayDate': '2014-03-18', 
        'minimumInvestmentAmount': 0.01, 'issuer': 'Irland, Republik', 'issueDate': '2014-01-14', 
        'issueVolume': 8030950000.0, 'circulatingVolume': 8030950000.0, 'issueCurrency': 'EUR', 
        'firstTradingDay': '2014-01-09', 'maturity': '2024-03-18', 
        'noticeType': None, 'extraordinaryCancellation': None, 'portfolioCurrency': 'EUR', 'subordinated': None, 
        'flatNotation': None, 'quotationType': {'originalValue': '2', 'translations':{'de': 'Prozentnotiert', 'en': 'Percent'}}  # noqa
        }
        """
    if not isinstance(instrument_data, dict):  # instrument data is dict, no dict means no data, proceed to next ISIN!
        return

    bid_ask_latest = bf4py.bonds.bid_ask_latest(isin=isin)
    """
    {'isin': 'IE00B6X95T99', 'bidLimit': 0.0, 'askLimit': 0.0, 'bidSize': 0.0, 'askSize': 0.0, 'lastPrice': 100.26, 
    'timestampLastPrice': '2023-05-12T17:00:17+02:00', 'changeToPrevDayAbsolute': 0.0, 'changeToPrevDayInPercent': 0, 
    'spreadAbsolute': 0, 'spreadRelative': 0, 'timestamp': '2023-05-12T17:30:00+02:00', 'nominal': True, 
    'tradingStatus': 'CLOSED', 'instrumentStatus': 'ACTIVE', 'open': 100.26}
    """
    instrument_data.update(bid_ask_latest)  # add bid_ask_latest dict to instrument_data dict

    return instrument_data


def extract_key_specs(data: dict):
    key_specs = {
        'ISIN': data['isin'],
        'issuer': data['issuer'],
        'coupon_%': data['cupon'],
        'last_price': data['lastPrice'],
        'maturity_date': data['maturity'],
        'website_url': f'https://www.boerse-frankfurt.de/bond/{data["isin"]}'
    }

    return key_specs


def calculate_metrics(specs_list: list, sell_date_str: str):
    date_str_format = '%Y-%m-%d'
    maturity_dates = []
    for bond in specs_list:
        """bond e.g.
        {'ISIN': 'XS1218821756', 'issuer': 'ABN AMRO Bank N.V.', 'coupon_%': 1.0, 'last_price': 95.16, 'maturity_date': '2025-04-16', 'website_url': 'https://www.boerse-frankfurt.de/bond/XS1218821756'}  # noqa
        """
        if isinstance(bond['maturity_date'], str):
            maturity_date_dt = datetime.strptime(bond['maturity_date'], date_str_format)
        else:
            # maturity_date empty (a.k.a. not-a-number nan, float type) when e.g. bond is perpetual
            maturity_date_dt = sell_date_str

        maturity_dates.append(maturity_date_dt)

    return maturity_dates


def csv_key_specs(specs_list: list, output_name: str):
    """sample list of specs:
    [{'ISIN': 'IE00B6X95T99', 'coupon_%': 3.4, 'maturity_date': '2024-03-18', 'website_url': 'https://www.boerse-frankfurt.de/bond/IE00B6X95T99'}, # noqa
    {'ISIN': 'XS0968913342', 'coupon_%': 5.125, 'maturity_date': None, 'website_url': 'https://www.boerse-frankfurt.de/bond/XS0968913342'}] # noqa
    """
    df = pd.DataFrame(specs_list)
    df = df.sort_values(by=['coupon_%'], ascending=False)  # first row = highest coupon %

    df.to_csv(f'{output_name}.csv', index=False)


# main('Book1.csv', 'degiro_bonds', '2024-10-01')
