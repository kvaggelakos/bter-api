# Copyright (c) 2013 Alan McIntyre

import httplib
import json
import decimal

decimal.getcontext().rounding = decimal.ROUND_DOWN
exps = [decimal.Decimal("1e-%d" % i) for i in range(16)]

domain = 'bter.com'

all_pairs = ['btc_cny',
             'ltc_cny',
             'ftc_cny',
             'frc_cny',
             'trc_cny',
             'wdc_cny',
             'yac_cny',
             'cnc_cny',
             'ftc_ltc',
             'frc_ltc',
             'ppc_ltc',
             'trc_ltc',
             'nmc_ltc',
             'wdc_ltc',
             'yac_ltc',
             'cnc_ltc',
             'bqc_ltc',
             'ltc_btc',
             'nmc_btc',
             'ppc_btc',
             'trc_btc',
             'frc_btc',
             'ftc_btc',
             'bqc_btc',
             'cnc_btc',
             'btb_btc',
             'yac_btc',
             'wdc_btc']

all_currencies = list(set(sum([p.split('_') for p in all_pairs], [])))
             
max_digits = {'btc_cny': {'price': 2, 'amount': 4},
              'ltc_cny': {'price': 2, 'amount': 4},
              'ftc_cny': {'price': 3, 'amount': 3},
              'frc_cny': {'price': 3, 'amount': 3},
              'trc_cny': {'price': 6, 'amount': 4},
              'wdc_cny': {'price': 6, 'amount': 4},
              'yac_cny': {'price': 6, 'amount': 4},
              'cnc_cny': {'price': 6, 'amount': 4},
              'ftc_ltc': {'price': 5, 'amount': 3},
              'frc_ltc': {'price': 5, 'amount': 3},
              'ppc_ltc': {'price': 6, 'amount': 4},
              'trc_ltc': {'price': 6, 'amount': 4},
              'nmc_ltc': {'price': 6, 'amount': 4},
              'wdc_ltc': {'price': 6, 'amount': 4},
              'yac_ltc': {'price': 6, 'amount': 4},
              'cnc_ltc': {'price': 6, 'amount': 4},
              'bqc_ltc': {'price': 6, 'amount': 4},
              'ltc_btc': {'price': 5, 'amount': 4},
              'nmc_btc': {'price': 6, 'amount': 4},
              'ppc_btc': {'price': 5, 'amount': 3},
              'trc_btc': {'price': 5, 'amount': 3},
              'frc_btc': {'price': 6, 'amount': 3},
              'ftc_btc': {'price': 5, 'amount': 3},
              'bqc_btc': {'price': 7, 'amount': 2},
              'cnc_btc': {'price': 6, 'amount': 3},
              'btb_btc': {'price': 5, 'amount': 4},
              'yac_btc': {'price': 6, 'amount': 3},
              'wdc_btc': {'price': 6, 'amount': 3}}

# min_orders = {'btc_cny': decimal.Decimal("0.1"),
#               'ltc_cny': decimal.Decimal("0.1"),
#               'ftc_cny': decimal.Decimal("0.1"),
#               'frc_cny': decimal.Decimal("0.1"),
#               'trc_cny': decimal.Decimal("0.1"),
#               'wdc_cny': decimal.Decimal("0.1"),
#               'yac_cny': decimal.Decimal("0.1"),
#               'cnc_cny': decimal.Decimal("0.1"),
#               'ftc_ltc': decimal.Decimal("0.1"),
#               'frc_ltc': decimal.Decimal("0.1"),
#               'ppc_ltc': decimal.Decimal("0.1"),
#               'trc_ltc': decimal.Decimal("0.1"),
#               'nmc_ltc': decimal.Decimal("0.1"),
#               'wdc_ltc': decimal.Decimal("0.1"),
#               'yac_ltc': decimal.Decimal("0.1"),
#               'cnc_ltc': decimal.Decimal("0.1"),
#               'bqc_ltc': decimal.Decimal("0.1"),
#               'ltc_btc': decimal.Decimal("0.1"),
#               'nmc_btc': decimal.Decimal("0.1"),
#               'ppc_btc': decimal.Decimal("0.1"),
#               'trc_btc': decimal.Decimal("0.1"),
#               'frc_btc': decimal.Decimal("0.1"),
#               'ftc_btc': decimal.Decimal("0.1"),
#               'bqc_btc': decimal.Decimal("0.1"),
#               'cnc_btc': decimal.Decimal("0.1"),
#               'btb_btc': decimal.Decimal("0.1"),
#               'yac_btc': decimal.Decimal("0.1"),
#               'wdc_btc': decimal.Decimal("0.1")}

fees = {'btc_cny': 0.002,
        'ltc_cny': 0.002,
        'ftc_cny': 0.002,
        'frc_cny': 0.002,
        'trc_cny': 0.002,
        'wdc_cny': 0.002,
        'yac_cny': 0.002,
        'cnc_cny': 0.002,
        'ftc_ltc': 0.002,
        'frc_ltc': 0.002,
        'ppc_ltc': 0.002,
        'trc_ltc': 0.002,
        'nmc_ltc': 0.002,
        'wdc_ltc': 0.002,
        'yac_ltc': 0.002,
        'cnc_ltc': 0.002,
        'bqc_ltc': 0.002,
        'ltc_btc': 0.002,
        'nmc_btc': 0.002,
        'ppc_btc': 0.002,
        'trc_btc': 0.002,
        'frc_btc': 0.002,
        'ftc_btc': 0.002,
        'bqc_btc': 0.002,
        'cnc_btc': 0.002,
        'btb_btc': 0.002,
        'yac_btc': 0.002,
        'wdc_btc': 0.002}


def parseJSONResponse(response):
    def parse_decimal(var):
        return decimal.Decimal(var)

    try:
        r = json.loads(response, parse_float=parse_decimal, parse_int=parse_decimal)
    except Exception as e:
        msg = "Error while attempting to parse JSON response: %s\nResponse:\n%r" % (e, response)
        raise Exception(msg)
    
    return r


class BTERConnection:
    def __init__(self, timeout=30):
        self.conn = httplib.HTTPSConnection(domain, timeout=timeout)
        
    def close(self):
        self.conn.close()
        
    def makeRequest(self, url, method='POST', extra_headers=None, params=''):
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        if extra_headers is not None:
            headers.update(extra_headers)
            
        self.conn.request(method, url, params, headers)
        response = self.conn.getresponse().read()
    
        return response
                                
    def makeJSONRequest(self, url, method='POST', extra_headers=None, params=""):
        response = self.makeRequest(url, method, extra_headers, params)
        return parseJSONResponse(response)
    
        
def validatePair(pair):
    if pair not in all_pairs:
        if "_" in pair:
            a, b = pair.split("_")
            swapped_pair = "%s_%s" % (b, a)
            if swapped_pair in all_pairs:
                msg = "Unrecognized pair: %r -- did you mean %s?" % (pair, swapped_pair)
                raise Exception(msg)
        raise Exception("Unrecognized pair: %r" % pair)


def truncateAmountDigits(value, digits):
    quantum = exps[digits]
    return decimal.Decimal(value).quantize(quantum)


def truncateAmount(value, pair, price_or_amount):
    return truncateAmountDigits(value, max_digits[pair][price_or_amount])


def formatCurrencyDigits(value, digits):
    s = str(truncateAmountDigits(value, digits))
    dot = s.index(".")
    while s[-1] == "0" and len(s) > dot + 2:
        s = s[:-1]
        
    return s


def formatCurrency(value, pair, price_or_amount):
    return formatCurrencyDigits(value, max_digits[pair][price_or_amount])