from services.initiate_fyers import InitiateFyers
from datetime import datetime
import logging
import discord
from pytz import timezone
import requests
import json
import os
from dotenv import load_dotenv


logging.basicConfig(filename='casterlyrock_logger.log', level=logging.DEBUG, format='%(asctime)s: %(levelname) -8s: - %(message)s',datefmt='%d-%b-%y %H:%M:%S')
#load_dotenv()


class BotUtils():

    async def getPositions(self) -> None:
            #Flow for Fyers
            logging.info("Inside : getPostions()")
            self.fyers_model = InitiateFyers().inititate_fyers()
            res = self.fyers_model.positions()
            logging.info(f"Inside : getPostions(): Response = {res}")
            MAX_LOSS_PERCENTAGE = 0.5
            openPositionDetails = []
            for position in res["netPositions"]:
                  if position['qty'] != 0 :
                        direction = 'LONG'
                        if position['side'] == 1:
                              direction = 'LONG'
                              averageBuy = position['buyAvg']
                              maxPossibleLossLong = (averageBuy * (MAX_LOSS_PERCENTAGE/100))*position['qty']
                              if position['unrealized_profit'] < 0  and abs(position['unrealized_profit']) > maxPossibleLossLong:
                                    logging.info("HARD SL on LONG Side")
                                    data = {}
                                    resExitPositions = self.fyers_model.exit_positions(data=data)

                        elif position['side'] == -1:
                              direction = 'SHORT'
                              averageSell = position['sellAvg']
                              maxPossibleLossShort = (averageSell * (MAX_LOSS_PERCENTAGE/100))*position['qty']
                              if position['unrealized_profit'] < 0  and abs(position['unrealized_profit']) > maxPossibleLossShort:
                                    logging.info("HARD SL on SHORT Side")
                                    data = {}
                                    resExitPositions = self.fyers_model.exit_positions(data=data)

                        positionDetails = f'{direction}-{position['symbol']} : {position['qty']} | {round(position['unrealized_profit'])}'
                        openPositionDetails.append(positionDetails)


            summary = f'''Total =  {round(res["overall"]['pl_total'])}, Realized = {round(res["overall"]['pl_realized'])},UnRealized = {round(res["overall"]['pl_unrealized'])}'''
            openPositionDetails.append(summary)
            result = '\n'.join(openPositionDetails)


            

            now = datetime.now(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
            messageColor = discord.Colour.red
            if res["overall"]['pl_unrealized'] > 0 :
                  messageColor = discord.Colour.green()
            elif res["overall"]['pl_unrealized'] <= 0 :
                  messageColor = discord.Colour.red()
            embdedMessage = discord.Embed(
                  colour=messageColor,
                  description=result,
                  title=f"Score Board at {now}"
            )

 
            ######################### DELTA_INDIA #################################
            # url = "https://cdn.india.deltaex.org/v2/positions/margined"
            

            # # Get open orders
            # payload = ''
            # method = 'GET'
            # timestamp = get_time_stamp()
            # path = 'v2/positions/margined'
            # query_string = '?product_id=27'
            # signature_data = method + timestamp + path + query_string + payload
            # signature = generate_signature('t0kOQBDVFIlMaQb5c0tp60KVnLDo9tnccU3xLFupIOnYSTGCZrMtATZMYrZE', signature_data)

            # req_headers = {
            # 'api-key': '4eXPFPDEU7vhQzzKfUcqgimKa0GH0U',
            # 'timestamp': timestamp,
            # 'signature': signature,
            # 'Content-Type': 'application/json'
            # }
            # query = {"product_id": 27}

            # response = requests.request(
            # method, url, data=payload, params=query, timeout=(3, 27), headers=req_headers
            # )

            # logging.info(response.json())
            # print(response.json())

            return embdedMessage
    
    async def refreshToken(self) -> None:
          self.fyers_model = InitiateFyers().refreshToken()

    async def kill(self) -> None:
          self.fyers_model = InitiateFyers().inititate_fyers()
          data = {}
          res = self.fyers_model.exit_positions(data=data)
          return res