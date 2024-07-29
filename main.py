import asyncio
import discord
from fastapi import FastAPI
from bot import bot
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World"}

@app.post("/send_message/")
async def send_message(channel_id: int, message: str):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
        return {"status": "Message sent"}
    else:
        return {"status": "Channel not found"}

async def start_bot():
    await bot.start('ADD_SECRETE_HERE')

async def main():
    bot_task = asyncio.create_task(start_bot())
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    api_task = asyncio.create_task(server.serve())
    await asyncio.wait([bot_task, api_task])

if __name__ == "__main__":
    asyncio.run(main())
