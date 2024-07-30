from services.initiate_fyers import InitiateFyers
from datetime import datetime
import logging
import discord

logging.basicConfig(filename='casterlyrock_logger.log', level=logging.DEBUG, format='%(asctime)s: %(levelname) -8s: - %(message)s',datefmt='%d-%b-%y %H:%M:%S')

class BotUtils():

    async def getPositions(self) -> None:
            logging.info("Inside : getPostions()")
            self.fyers_model = InitiateFyers().inititate_fyers()
            res = self.fyers_model.positions()
            openPositionDetails = []
            for position in res["netPositions"]:
                  if position['realized_profit'] == 0 :
                        direction = 'BUY'
                        if position == 1:
                              direction = 'LONG'
                        elif position == -1:
                            direction = 'SHORT'
                        positionDetails = f'{direction}-{position['symbol']} : {position['qty']} | {round(position['unrealized_profit'])}'
                        openPositionDetails.append(positionDetails)

            summary = f'''Total =  {round(res["overall"]['pl_total'])}, Realized = {round(res["overall"]['pl_realized'])},UnRealized = {round(res["overall"]['pl_unrealized'])}'''
            openPositionDetails.append(summary)
            result = '\n'.join(openPositionDetails)

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
            return embdedMessage
    
    async def refreshToken(self) -> None:
          self.fyers_model = InitiateFyers().refreshToken()

    async def kill(self) -> None:
          self.fyers_model = InitiateFyers().inititate_fyers()
          data = {}
          res = self.fyers_model.exit_positions(data=data)
          return res