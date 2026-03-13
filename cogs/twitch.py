import discord
from discord.ext import commands

class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Module Twitch prêt à l\'emploi.')

async def setup(bot):
    await bot.add_cog(Twitch(bot))