from bf4py import BF4Py
import csv
import pandas as pd
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s Local >>> %(message)s',
                    datefmt='%Y%m%d %H:%M:%S')


def main(degiro_csv: str, output_name: str):
    """
    TODO: get latest price
    TODO: get company details - industry, latest news
    TODO: calculate profit based on price, coupon and maturity e.g. AT0000383864
    TODO: from a selection of bonds with their specifics, input an end date, calculate bond with highest profit?
    """
    isin_list = extract_csv_isin(degiro_csv)
    specs_list = list_key_specs(isin_list)
    csv_key_specs(specs_list, output_name)


def extract_csv_isin(filename: str):
    with open(f'{filename}.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        info_list = []
        for row in csv_reader:
            info = {}
            if row[1] == '':  # rows with ISIN also have a second not-empty Curency column
                continue

            info['isin'] = row[0][-12:]  # some values in 'ISIN' column have more than ISIN, e.g. 'OETM | AT0000A0DXC2'
            info['lastPrice'] = (float(row[2][2:].replace(',', '.')) if ',' in row[2][2:]
                                 else '')
            info_list.append(info)

    logging.info(f'run.extract_csv_isin - last isin in isin_list is {info_list[-1]}')
    return info_list


def list_key_specs(info_list: list):
    bf4py = BF4Py(default_isin='XS0968913342', default_mic='XFRA')
    logging.info('run.list_key_specs - class object bf4py initialized')
    specs_list = []
    for info in info_list:
        try:
            data = get_bond_data(bf4py, info['isin'])
            data = {**data, **info}
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


def csv_key_specs(specs_list: list, output_name: str):
    """sample list of specs:
    [{'ISIN': 'IE00B6X95T99', 'coupon_%': 3.4, 'maturity_date': '2024-03-18', 'website_url': 'https://www.boerse-frankfurt.de/bond/IE00B6X95T99'}, # noqa
    {'ISIN': 'XS0968913342', 'coupon_%': 5.125, 'maturity_date': None, 'website_url': 'https://www.boerse-frankfurt.de/bond/XS0968913342'}] # noqa
    """
    df = pd.DataFrame(specs_list)

    df.to_csv(f'{output_name}.csv', index=False)


main('input', 'output')
