from services.initiate_fyers import InitiateFyers
from services.models.fyers_response_model import FyersFundsResponse
from services.models.enumeration import FundBalanceType
import logging
logger = logging.getLogger()

def get_account_balance(fund_balance_type):
    print("**************************GET ACCOUNT BALANCE**************************************")
    response = InitiateFyers().inititate_fyers().funds()
    #print(response)
    if response and 'fund_limit' in response:
        for fund in response["fund_limit"]:
            if 'title' in fund and 'equityAmount' in fund and fund['title'] == fund_balance_type:
                return fund["equityAmount"]

def find_premium_price(symbol_obj):
    response = InitiateFyers().inititate_fyers().quotes(data=symbol_obj)
    print("**************************FIND PREMIUM PRICE**************************************")
    #print(response)
    if response and 'd' in response:
        for symbol in response["d"]:
            if 'n' in symbol and symbol['n'] == symbol_obj['symbols'] and 'v' in symbol:
                return symbol['v']['lp']

def Calculate_positon_size(provided_sl, available_balance, last_traded_price):
    max_loss_percentage=0.02
    lot_size = 15
    #print(available_balance)
    max_allowed_stop_loss_value = available_balance * max_loss_percentage
    expected_loss_per_unit = last_traded_price - provided_sl
    expected_max_unit = max_allowed_stop_loss_value / expected_loss_per_unit
    expected_number_of_lots = round(expected_max_unit / lot_size)
    print(f"Number of Lots {expected_number_of_lots}")
    return expected_number_of_lots

# account_balance = get_account_balance(FundBalanceType.AVAILABLE_BALANCE.value)
# premium = find_premium_price( {"symbols":"NSE:BANKNIFTY2470352300PE"})
# Calculate_positon_size(298, account_balance, premium)