from services.initiate_fyers import InitiateFyers
from services.util import get_account_balance, find_premium_price, Calculate_positon_size
from services.models.enumeration import FundBalanceType
from services.models.fyers_response_model import OrderDetails 

class PlaceOrder():

    def __init__(self) -> None:
        pass

    def place_order(self, orderDetails: OrderDetails) -> None:
        self.fyers_model = InitiateFyers().inititate_fyers()
        account_balance = get_account_balance(FundBalanceType.AVAILABLE_BALANCE.value)
        premium = find_premium_price( {"symbols":orderDetails.symbol})
        lot_size = Calculate_positon_size(orderDetails.stop_loss, account_balance, premium)
        quantity_to_buy = lot_size * 15
#        print(lot_size)
        stop_loss_in_point = premium - orderDetails.stop_loss
        take_profit = stop_loss_in_point * 2.25
        data = {
            "symbol":orderDetails.symbol,
            "qty": quantity_to_buy,
            "type":1,
            "side":1,
            "productType":"BO",
            "limitPrice": premium + 2,
            "stopPrice": 0,
            "validity":"DAY",
            "disclosedQty":0,
            "offlineOrder":True,
            "stopLoss": orderDetails.stop_loss,
            "takeProfit": premium + take_profit
        }
        print(data)
        response = self.fyers_model.place_order(data=data)
        print(response)
        return response

#obj = {
#            "symbol":"NSE:BANKNIFTY2470352300PE",
#            "stop_loss": 298
#        }
#if __name__ == '__main__':
#    PlaceOrder().place_order(obj)