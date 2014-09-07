# Copyright (c) 2013 Alan McIntyre

import datetime
import decimal

from bterapi import common


def getDepth(pair, connection=None, error_handler=None):
    """
    Retrieve the depth for the given pair. Returns a tuple (asks, bids);
    each of these is a list of (price, volume) tuples.
    """
    common.validatePair(pair)

    if connection is None:
        connection = common.BTERConnection()

    depth = common.validateResponse(connection.makeJSONRequest('/api/1/depth/%s' % pair, method='GET'),
                                    error_handler=error_handler)

    if type(depth) is not dict:
        raise TypeError("The response is not a dict.")

    asks = depth.get('asks')
    if type(asks) is not list:
        raise TypeError("The response does not contain an asks list.")

    bids = depth.get('bids')
    if type(bids) is not list:
        raise TypeError("The response does not contain a bids list.")

    return asks, bids


class Trade(object):
    __slots__ = ('pair', 'type', 'price', 'tid', 'amount', 'date')

    def __init__(self, **kwargs):
        for s in Trade.__slots__:
            setattr(self, s, kwargs.get(s))

        if type(self.date) in (int, float, decimal.Decimal):
            self.date = datetime.datetime.fromtimestamp(self.date)
        elif type(self.date) is str:
            if "." in self.date:
                self.date = datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S.%f")
            else:
                self.date = datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S")


def getTradeHistory(pair, connection=None, start_tid=None, count=None, error_handler=None):
    """
    Retrieve the trade history for the given pair. Returns a list of
    Trade instances. If count is not None, it should be an integer, and
    specifies the number of items from the trade history that will be
    processed and returned.
    """
    common.validatePair(pair)

    if connection is None:
        connection = common.BTERConnection()

    if start_tid is None:
        result = connection.makeJSONRequest('/api/1/trade/%s' % pair, method='GET')
    else:
        result = connection.makeJSONRequest('/api/1/trade/%s/%d' % (pair, start_tid), method='GET')

    result = common.validateResponse(result, error_handler=error_handler)

    history = result[u'data']
    if type(history) is not list:
        raise Exception('The response does not contain a history list.')

    result = []
    # Limit the number of items returned if requested.
    if count is not None:
        history = history[:count]

    for h in history:
        h["pair"] = pair
        t = Trade(**h)
        result.append(t)
    return result
