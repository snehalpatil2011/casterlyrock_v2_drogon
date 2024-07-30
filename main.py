from fastapi import FastAPI
from services.place_order import PlaceOrder
from services.models.fyers_response_model import OrderDetails,TwinTowerDetails,OrderBankNiftyFutureDetails
import uvicorn
import asyncio
import discord
from fastapi import FastAPI
from services.bot import bot,sendMessageToChannel
import uvicorn
import os
import logging

logging.basicConfig(filename='casterlyrock_logger.log', level=logging.DEBUG, format='%(asctime)s: %(levelname) -8s: - %(message)s',datefmt='%d-%b-%y %H:%M:%S')

app = FastAPI()

@app.get("/")
async def health_check():
    logging.info("Health Check called !")
    return "The health check is Successfull !"

@app.post("/send_message_discord/")
async def send_message(channel_id: int, message: str):
    await sendMessageToChannel(message)
    

@app.post("/placeorder")
async def place_order(orderDetails:OrderDetails):
    logging.info(f"Webhook Triggered | Placing orders with details : Symbol :  {orderDetails.symbol} , SL : {orderDetails.stop_loss}")
    resp = PlaceOrder().place_order(orderDetails)
    return resp

@app.get("/twintowersdaily")
async def generate_twin_towers():
    logging.info("Twin Tower Generation Started !")
    idenitfied_symbols_pp = PlaceOrder().twinTowerGenerator("D",20)
    return idenitfied_symbols_pp

@app.post("/orderbankniftyfuture")
async def place_order_bank_nifty_future(orderBankNiftyFutureDetails:OrderBankNiftyFutureDetails):
    logging.info("Request Received : Place order for BANK NIFTY FUTURES")
    placer = PlaceOrder()
    res = await placer.place_order_bank_nifty_future(orderBankNiftyFutureDetails)
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
