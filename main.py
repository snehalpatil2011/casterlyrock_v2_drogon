from fastapi import FastAPI
from services.place_order import PlaceOrder
from services.models.fyers_response_model import OrderDetails,TwinTowerDetails,OrderPlacerInputPayload
import uvicorn
import asyncio
import discord
from fastapi import FastAPI
from services.bot import bot,sendMessageToChannel
import uvicorn
import os
import logging
import services.symbol_mapper as symbolMapper

logging.basicConfig(filename='casterlyrock_logger.log', level=logging.DEBUG, format='%(asctime)s: %(levelname) -8s: - %(message)s',datefmt='%d-%b-%y %H:%M:%S')

app = FastAPI()

@app.get("/")
async def health_check():
    logging.info("Health Check called !")
    return "The health check is Successfull !"

@app.post("/send_message_discord/")
async def send_message(channel_id: int, message: str):
    await sendMessageToChannel(message)
    

# @app.post("/placeorder")
# async def place_order(orderDetails:OrderDetails):
#     logging.info(f"Webhook Triggered | Placing orders with details : Symbol :  {orderDetails.symbol} , SL : {orderDetails.stop_loss}")
#     resp = PlaceOrder().place_order(orderDetails)
#     return resp

@app.get("/twintowersdaily")
async def generate_twin_towers():
    logging.info("Twin Tower Generation Started !")
    idenitfied_symbols_pp = PlaceOrder().twinTowerGenerator("D",20)
    return idenitfied_symbols_pp

@app.post("/orderplacer")
async def order_placer(orderPlacerInputPayload:OrderPlacerInputPayload):
    if orderPlacerInputPayload.broker == "FYERS":
        logging.info(f"Request Received : Place order for {orderPlacerInputPayload.symbol}")
        logging.info(f"BROKER : {orderPlacerInputPayload.broker}")
        orderPlacerInputPayload.symbol = orderPlacerInputPayload.symbol.replace(orderPlacerInputPayload.exchange + ":", "")
        rootSymbol = symbolMapper.get_root_symbol(orderPlacerInputPayload.symbol)
        orderPlacerInputPayload.symbol = symbolMapper.convert_tradingview_to_fyers(orderPlacerInputPayload.symbol,orderPlacerInputPayload.exchange)
        logging.info(f"SYMBOL CONVERSION : Coverted to FYERS and new value is {orderPlacerInputPayload.symbol}")
        placer = PlaceOrder()
        res = await placer.order_placer_fyers_delegate(orderPlacerInputPayload,rootSymbol)
        return res
    if orderPlacerInputPayload.broker == "DELTA_INDIA":
        logging.info(f"Request Received : Place order for {orderPlacerInputPayload.symbol}")
        logging.info(f"BROKER : {orderPlacerInputPayload.broker}")
        placer = PlaceOrder()
        res = await placer.order_placer_delta_india_delegate(orderPlacerInputPayload)
        return res

@app.get("/accountDetails")
async def getAccountDetails():
    logging.info("Request Received : Get Account Details")
    placer = PlaceOrder()
    res = await placer.get_account_details()
    return res

async def start_bot():
    await bot.start(os.environ.get('MY_WORD'))

async def main():
    bot_task = asyncio.create_task(start_bot())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())
    await asyncio.wait([bot_task, api_task])

if __name__ == "__main__":
    asyncio.run(main())
