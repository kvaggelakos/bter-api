from bterapi import common

class Ticker:
    _market_data = {}

    def __init__(self, pairs=common.all_pairs):
        for pair in pairs: common.validatePair(pair)
        self._pairs = pairs
        self._all = self._pairs == common.all_pairs

    def update(self):
        connection = common.BTERConnection()
        if self._all:
            self._market_data = connection.makeJSONRequest("/api/1/tickers", method="GET")
        else:
            self._market_data = dict((pair, connection.makeJSONRequest("/api/1/ticker/%s" % pair, method="GET")) for pair in self.pairs)

    @property
    def pairs(self):
        return self._pairs

    @property
    def market_data(self):
        return self._market_data

