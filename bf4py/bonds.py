#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import date, datetime, timezone, time

from .connector import BF4PyConnector


class Bonds():
    def __init__(self, connector: BF4PyConnector = None, default_isin=None, default_mic='XETR'):
        self.default_isin = default_isin
        self.default_mic = default_mic

        if connector is None:
            self.connector = BF4PyConnector()
        else:
            self.connector = connector

    def instrument_data(self, isin: str = None, mic: str = None):
        """
        Returns all information about given derivative ISIN.

        Parameters
        ----------
        isin : str
            ISIN ov valid derivative.

        Returns
        -------
        data : TYPE
            Dict with information.

        """
        if isin is None:
            isin = self.default_isin
        assert isin is not None, 'No ISIN given'
        if mic is None:
            mic = self.default_mic
        assert mic is not None, 'No mic (Exchange) given'

        params = {'isin': isin,
                  'mic': mic}

        data = self.connector.data_request('master_data_bond', params)

        return data

    def bid_ask_latest(self, isin: str = None, mic: str = None):
        """
        Returns all information about given derivative ISIN.

        Parameters
        ----------
        isin : str
            ISIN ov valid derivative.

        Returns
        -------
        data : TYPE
            Dict with information.

        """
        if isin is None:
            isin = self.default_isin
        assert isin is not None, 'No ISIN given'
        if mic is None:
            mic = self.default_mic
        assert mic is not None, 'No mic (Exchange) given'

        params = {'isin': isin,
                  'mic': mic}

        #data = self.connector.data_request('performance', params)
        #data = self.connector.data_request('interest_rate_widget', params)
        data = self.connector.data_request('quote_box/single', params)

        return data