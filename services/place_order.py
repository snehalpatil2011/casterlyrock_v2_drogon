from services.initiate_fyers import InitiateFyers
from services.util import get_account_balance, find_premium_price, Calculate_positon_size,calculate_total_quantity
from services.models.enumeration import FundBalanceType
from services.models.fyers_response_model import OrderDetails,OrderPlacerInputPayload
from services.initiate_delta_india import generate_signature
from datetime import datetime,timedelta
import time
import logging
from services.bot import bot,sendMessageToChannel
import json
import requests
import os
from dotenv import load_dotenv

logging.basicConfig(filename='casterlyrock_logger.log', level=logging.DEBUG, format='%(asctime)s: %(levelname) -8s: - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
load_dotenv()


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

    async def order_placer_fyers_delegate(self, orderPlacerInputPayload: OrderPlacerInputPayload,rootSymbol: str) -> None:
        logging.info("Inside : Handler Method - PlaceOrder().order_placer_fyers_delegate()")
        await sendMessageToChannel("Inside : Handler Method - PlaceOrder().order_placer_fyers_delegate()")
        quanity = calculate_total_quantity(rootSymbol,orderPlacerInputPayload.numberOfLots)
        self.fyers_model = InitiateFyers().inititate_fyers()

        #Verify Order Validity
        positionsres = self.fyers_model.positions()
        openPositionsCount = positionsres["overall"]['count_open']
        if orderPlacerInputPayload.signalType == 'LONG_ENTRY' or orderPlacerInputPayload.signalType == 'SHORT_ENTRY':
            if(openPositionsCount > 0):
                logging.info(f"ISSUE: There was already a open position while serving request for {orderPlacerInputPayload.signalType}. Hence we will discard the request")
                await sendMessageToChannel(f"ISSUE: There was already a open position while serving request for {orderPlacerInputPayload.signalType}.Hence we will discard the request")
                return f"Request no Completed. As the Request for {orderPlacerInputPayload.signalType} was incorrect."

        if orderPlacerInputPayload.signalType == 'LONG_EXIT' or orderPlacerInputPayload.signalType == 'SHORT_EXIT':
            if(openPositionsCount == 0):
                logging.info(f"ISSUE: There were no open position while serving request for {orderPlacerInputPayload.signalType}.Hence we will discard the request")
                await sendMessageToChannel(f"ISSUE: There were no open position while serving request for {orderPlacerInputPayload.signalType}.Hence we will discard the request")
                return f"Request no Completed. As the Request for {orderPlacerInputPayload.signalType} was incorrect."

        #DEFAULT = BUY
        if orderPlacerInputPayload.signalType == 'LONG_ENTRY' or orderPlacerInputPayload.signalType == 'SHORT_EXIT' :
            print("Preparing Buy Order")
            #BUY_SIDE
            data = {
                "symbol": orderPlacerInputPayload.symbol,
                "qty": quanity,
                "type":2,
                "side":1,
                "productType":"INTRADAY",
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":orderPlacerInputPayload.offlineOrder,
                "orderTag":str.replace(orderPlacerInputPayload.signalType,"_","")
            }
            logging.info(f"Submitting BUY Order for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Order with Details : {data}")
            await sendMessageToChannel(f"Submitting BUY Order for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Order with Details : {data}")
            res = self.fyers_model.place_order(data=data)
            logging.info(f"Received Response after order submitted for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Response with Details : {res}")
            await sendMessageToChannel(f"Received Response after order submitted for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Response with Details : {res}")
            return res

        
        if orderPlacerInputPayload.signalType == 'SHORT_ENTRY' or orderPlacerInputPayload.signalType == 'LONG_EXIT' :
            #SELL SIDE
            data = {
                "symbol":orderPlacerInputPayload.symbol,
                "qty":quanity,
                "type":2,
                "side":-1,
                "productType":"INTRADAY",
                "limitPrice":0,
                "stopPrice":0,
                "validity":"DAY",
                "disclosedQty":0,
                "offlineOrder":orderPlacerInputPayload.offlineOrder,
                "orderTag":str.replace(orderPlacerInputPayload.signalType,"_","")
            }
            logging.info(f"Submitting BUY Order for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Order with Details : {data}")
            await sendMessageToChannel(f"Submitting BUY Order for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Order with Details : {data}")
            res = self.fyers_model.place_order(data=data)
            logging.info(f"Received Response after order submitted for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Response with Details : {res}")
            await sendMessageToChannel(f"Received Response after order submitted for Symbol [{orderPlacerInputPayload.symbol}] for Signal - [{orderPlacerInputPayload.signalType}] Response with Details : {res}")
            return res

    async def order_placer_delta_india_delegate(self, orderPlacerInputPayload: OrderPlacerInputPayload) -> None:
        logging.info("Inside : Handler Method - PlaceOrder().order_placer_delta_india_delegate()")
        #await sendMessageToChannel("Inside : Handler Method - PlaceOrder().order_placer_delta_india_delegate()")

        # Prepare the order data
        #DEFAULT = BUY
        if orderPlacerInputPayload.signalType == 'LONG_ENTRY' or orderPlacerInputPayload.signalType == 'SHORT_EXIT' :
            order_data = {
                'product_id': 27,  # Product ID for BTCUSD is 27
                'size': orderPlacerInputPayload.numberOfLots,
                'order_type': 'market_order',
                'side': 'buy'
            }

            body = json.dumps(order_data, separators=(',', ':'))
            method = 'POST'
            endpoint = '/v2/orders'
            signature, timestamp = generate_signature(method, endpoint, body)
            # Add the API key and signature to the request headers
            headers = {
                'api-key': os.getenv('API_KEY_DELTA_INDIA'),
                'signature': signature,
                'timestamp': timestamp,
                'Content-Type': 'application/json'
            }
            response = requests.post('https://cdn.india.deltaex.org/v2/orders', headers=headers, data=body)
            order_response = response.json()
            print(order_response)
            return order_response
        
        if orderPlacerInputPayload.signalType == 'SHORT_ENTRY' or orderPlacerInputPayload.signalType == 'LONG_EXIT' :
            order_data = {
                'product_id': 27,  # Product ID for BTCUSD is 27
                'size': orderPlacerInputPayload.numberOfLots,
                'order_type': 'market_order',
                'side': 'sell'
            }

            body = json.dumps(order_data, separators=(',', ':'))
            method = 'POST'
            endpoint = '/v2/orders'
            signature, timestamp = generate_signature(method, endpoint, body)
            # Add the API key and signature to the request headers
            headers = {
                'api-key': os.getenv('API_KEY_DELTA_INDIA'),
                'signature': signature,
                'timestamp': timestamp,
                'Content-Type': 'application/json'
            }
            response = requests.post('https://cdn.india.deltaex.org/v2/orders', headers=headers, data=body)
            order_response = response.json()
            print(order_response)
            return order_response



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