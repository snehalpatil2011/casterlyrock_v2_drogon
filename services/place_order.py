from services.initiate_fyers import InitiateFyers
from services.util import get_account_balance, find_premium_price, Calculate_positon_size
from services.models.enumeration import FundBalanceType
from services.models.fyers_response_model import OrderDetails,OrderBankNiftyFutureDetails
from datetime import datetime,timedelta
import time
import logging
from services.bot import bot,sendMessageToChannel

logging.basicConfig(filename='casterlyrock_logger.log', level=logging.DEBUG, format='%(asctime)s: %(levelname) -8s: - %(message)s',datefmt='%d-%b-%y %H:%M:%S')


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
            "limitPrice": round(premium + 2),
            "stopPrice": 0,
            "validity":"DAY",
            "disclosedQty":0,
            "offlineOrder":False,
            "stopLoss": round(stop_loss_in_point),
            "takeProfit": round(take_profit)
        }
        print(data)
        response = self.fyers_model.place_order(data=data)
        print(response)
        return response
    
    #read file
    def twinTowerGenerator(self,timeperiod, daysOffset) -> None:
        print("STARTED :  Twin Tower Gnerator")
        self.fyers_model = InitiateFyers().inititate_fyers()

        #Identify start and end date
        startDateDerived = datetime.today().strftime('%Y-%m-%d')
        print(f"Derived Start Date = {startDateDerived}")
        endDateDerived = (datetime.today() - timedelta(days=daysOffset)).strftime('%Y-%m-%d')
        print(f"Derived End Date = {endDateDerived}")

        input_stock_file = open("stock_list.txt","r")
        file_content = input_stock_file.readline()
        symbols = file_content.split(",")
        #print(symbols)
        idenitfied_symbols_pp = []
        for symbol in symbols:
            time.sleep(0.2)
            print(f"Processing Symbol = {symbol}")
            #PlaceOrder().isTwinTower(symbol)
            data = {
                "symbol": symbol+"-EQ",
                "resolution":timeperiod,
                "date_format":"1",
                "range_from": endDateDerived,
                "range_to": startDateDerived,
                "cont_flag":"1"
                }
            response = self.fyers_model.history(data=data)
            #print(response)
            candles1 = response['candles']
            candles = candles1[-11:]
            candle_open = candles[len(candles)-1][1]
            candle_close = candles[len(candles)-1][4]
            up_day = True if candle_close > candle_open else False
            down_day = True if candle_close <= candle_open else False
            last_candleVolume = candles[len(candles) - 1][5]
            #print(f"Most Recent Candle : Open = {candle_open}, Close = {candle_close}, Upday = {up_day},DownDay = {down_day},lastCandleVolume = {last_candleVolume}")
            PPVol = 0
            for i in range(len(candles) - 1):
                candle_volume = candles[i][5]
                if candles[len(candles) - 1][5] > candles[i][5]:
                    PPVol = PPVol + 1
                else:
                    PPVol = 0
                #print(f"Candle : Volume = {candle_volume}")
                #print(f"Las Candle Volume = {candles[len(candles) - 1]}")
            if PPVol == len(candles)-1 and up_day:
                #print(f"{symbol} | PIVOT:True")
                idenitfied_symbols_pp.append(symbol)
        #print(idenitfied_symbols_pp)
        return idenitfied_symbols_pp

    async def place_order_bank_nifty_future(self, orderBankNiftyFutureDetails: OrderBankNiftyFutureDetails) -> None:
        logging.info("Inside : Handler Method - PlaceOrder().place_order_bank_nifty_future()")
        await sendMessageToChannel("Inside : Handler Method - PlaceOrder().place_order_bank_nifty_future()")
        LOT_SIZE = 15
        self.fyers_model = InitiateFyers().inititate_fyers()

        #Verify Order Validity
        positionsres = self.fyers_model.positions()
        openPositionsCount = positionsres["overall"]['count_open']
        if orderBankNiftyFutureDetails.signalType == 'LONG_ENTRY' or orderBankNiftyFutureDetails.signalType == 'SHORT_ENTRY':
            if(openPositionsCount > 0):
                logging.info(f"ISSUE: There was already a open position while serving request for {orderBankNiftyFutureDetails.signalType}. Hence we will discard the request")
                await sendMessageToChannel(f"ISSUE: There was already a open position while serving request for {orderBankNiftyFutureDetails.signalType}.Hence we will discard the request")
                return f"Request no Completed. As the Request for {orderBankNiftyFutureDetails.signalType} was incorrect."

        if orderBankNiftyFutureDetails.signalType == 'LONG_EXIT' or orderBankNiftyFutureDetails.signalType == 'SHORT_EXIT':
            if(openPositionsCount == 0):
                logging.info(f"ISSUE: There were no open position while serving request for {orderBankNiftyFutureDetails.signalType}.Hence we will discard the request")
                await sendMessageToChannel(f"ISSUE: There were no open position while serving request for {orderBankNiftyFutureDetails.signalType}.Hence we will discard the request")
                return f"Request no Completed. As the Request for {orderBankNiftyFutureDetails.signalType} was incorrect."

        #DEFAULT = BUY
        if orderBankNiftyFutureDetails.signalType == 'LONG_ENTRY' or orderBankNiftyFutureDetails.signalType == 'SHORT_EXIT' :
            print("Preparing Buy Order")
            #BUY_SIDE
            data = {
                "symbol": orderBankNiftyFutureDetails.symbol,
                "qty": LOT_SIZE,
                "type":2,
                "side":1,
                "productType":"INTRADAY",
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
                "orderTag":str.replace(orderBankNiftyFutureDetails.signalType,"_","")
            }
            logging.info(f"Submitting BUY Order for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Order with Details : {data}")
            await sendMessageToChannel(f"Submitting BUY Order for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Order with Details : {data}")
            res = self.fyers_model.place_order(data=data)
            logging.info(f"Received Response after order submitted for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Response with Details : {res}")
            await sendMessageToChannel(f"Received Response after order submitted for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Response with Details : {res}")
            return res

        
        if orderBankNiftyFutureDetails.signalType == 'SHORT_ENTRY' or orderBankNiftyFutureDetails.signalType == 'LONG_EXIT' :
            #SELL SIDE
            data = {
                "symbol":orderBankNiftyFutureDetails.symbol,
                "qty":LOT_SIZE,
                "type":2,
                "side":-1,
                "productType":"INTRADAY",
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":False,
                "orderTag":str.replace(orderBankNiftyFutureDetails.signalType,"_","")
            }
            logging.info(f"Submitting BUY Order for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Order with Details : {data}")
            await sendMessageToChannel(f"Submitting BUY Order for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Order with Details : {data}")
            res = self.fyers_model.place_order(data=data)
            logging.info(f"Received Response after order submitted for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Response with Details : {res}")
            await sendMessageToChannel(f"Received Response after order submitted for Symbol [{orderBankNiftyFutureDetails.symbol}] for Signal - [{orderBankNiftyFutureDetails.signalType}] Response with Details : {res}")
            return res

    async def get_account_details(self) -> None:
        logging.info("Inside : Handler Method - PlaceOrder().get_account_details()")
        await sendMessageToChannel("Inside : Handler Method - PlaceOrder().get_account_details()")
        self.fyers_model = InitiateFyers().inititate_fyers()
        res = self.fyers_model.funds()
        logging.info(f"RESULT(accountDetails): {res}")
        await sendMessageToChannel(f"RESULT(accountDetails): {res}")
        return res


#obj = {
#            "symbol":"NSE:BANKNIFTY2470352300PE",
#            "stop_loss": 298
#        }
#if __name__ == '__main__':
#    PlaceOrder().place_order(obj)

#if __name__ == '__main__':
#    PlaceOrder().twinTowerGenerator()