# Copyright (c) 2013 Alan McIntyre

import decimal
from .bterconnection import BTERConnection, parseJSONResponse

decimal.getcontext().rounding = decimal.ROUND_DOWN
exps = [decimal.Decimal("1e-%d" % i) for i in range(16)]

all_pairs = [
    "btc_cny",
    "ltc_cny",
    "bc_cny",
    "bitcny_cny",
    "bqc_cny",
    "btb_cny",
    "btq_cny",
    "btsx_cny",
    "cent_cny",
    "cmc_cny",
    "cnc_cny",
    "dgc_cny",
    "doge_cny",
    "drk_cny",
    "dtc_cny",
    "dvc_cny",
    "exc_cny",
    "ftc_cny",
    "frc_cny",
    "ifc_cny",
    "max_cny",
    "mec_cny",
    "mint_cny",
    "mmc_cny",
    "net_cny",
    "nmc_cny",
    "nxt_cny",
    "ppc_cny",
    "pts_cny",
    "qrk_cny",
    "red_cny",
    "src_cny",
    "tag_cny",
    "tips_cny",
    "tix_cny",
    "vrc_cny",
    "vtc_cny",
    "wdc_cny",
    "xcp_cny",
    "xmr_cny",
    "xpm_cny",
    "yac_cny",
    "zcc_cny",
    "zet_cny",
    "btc_usd",
    "bitusd_usd",
    "ltc_usd",
    "doge_usd",
    "drk_usd",
    "nxt_usd",
    "xcp_usd",
    "btsx_usd",
    "ltc_btc",
    "ac_btc",
    "aur_btc",
    "bc_btc",
    "bqc_btc",
    "btb_btc",
    "btcd_btc",
    "btsx_btc",
    "buk_btc",
    "c2_btc",
    "cdc_btc",
    "comm_btc",
    "cmc_btc",
    "cnc_btc",
    "dgc_btc",
    "doge_btc",
    "drk_btc",
    "drkc_btc",
    "dtc_btc",
    "exc_btc",
    "flt_btc",
    "frc_btc",
    "frsh_btc",
    "ftc_btc",
    "gml_btc",
    "kdc_btc",
    "lts_btc",
    "max_btc",
    "mec_btc",
    "mint_btc",
    "mmc_btc",
    "nav_btc",
    "nec_btc",
    "nmc_btc",
    "nas_btc",
    "net_btc",
    "nfd_btc",
    "nxt_btc",
    "ntx_btc",
    "ppc_btc",
    "prt_btc",
    "pts_btc",
    "qrk_btc",
    "rox_btc",
    "sfr_btc",
    "slm_btc",
    "src_btc",
    "tag_btc",
    "yac_btc",
    "via_btc",
    "vrc_btc",
    "vtc_btc",
    "wdc_btc",
    "xc_btc",
    "xcn_btc",
    "xcr_btc",
    "xcp_btc",
    "xpm_btc",
    "xmr_btc",
    "qora_btc",
    "zcc_btc",
    "zet_btc",
    "cent_ltc",
    "dvc_ltc",
    "ifc_ltc",
    "net_ltc",
    "nfd_ltc",
    "red_ltc",
    "tips_ltc",
    "tix_ltc",
    "bc_nxt",
    "btsx_nxt",
    "xcp_nxt",
    "btc_bitusd",
    "mgw_btc",
    "nxtty_btc",
    "token_btc",
    "token_nxt",
    "token_cny",
    "token_btcd"
]
all_currencies = list(set(sum([p.split('_') for p in all_pairs], [])))

max_digits = dict((pair, {"price": 8, "amount": 8}) for pair in all_pairs)

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

fees = {k: 0.001 for k in max_digits.keys()}

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


def validateResponse(result, error_handler=None):
    #TODO: Proper error handling with Exception sublcass
    if type(result) is not dict:
        raise Exception('The response is not a dict.')

    if not result[u'result'] or result[u'result'].lower() == u'false' or not result[u'result']:
        if error_handler is None:
            raise Exception(errorMessage(result))
        else:
            result = error_handler(result)

    return result


def errorMessage(result):
    if u'message' in result.keys():
        message = result[u'message']
    elif u'msg' in result.keys():
        message = result[u'msg']
    else:
        message = result
    return message
