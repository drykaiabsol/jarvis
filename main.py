import discord
import os
import asyncio
from discord.ext import commands
from config import DISCORD_TOKEN
from logger import setup_logger
from database.models import init_db

log = setup_logger("main")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = "/", intents = intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            log.info(f"Système {filename[:-3]} activé.")

@bot.event
async def on_ready():
    await init_db()
    log.info(f"J.A.R.V.I.S. est en ligne sous le nom : {bot.user}")
    log.info('Initialisé')

async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())