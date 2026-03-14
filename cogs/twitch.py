import discord
from discord.ext import commands, tasks
import aiohttp
import os

class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client_id = os.getenv('TWITCH_CLIENT_ID')
        self.client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.streamer_name = "drykai_"
        self.is_live = False
        self.check_twitch.start()

    def cog_unload(self):
        self.check_twitch.cancel()

    async def get_access_token(self):
        url = f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials"
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                data = await response.json()
                return data.get('access_token')
            
    @tasks.loop(minutes=2.0)
    async def check_twitch(self):
        token = await self.get_access_token()
        if not token:
            print(" Impossible de récupérer le token Twitch. ")
            return
        
        headers = {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {token}"
        }
        url = f"https://api.twitch.tv/helix/streams?user_login={self.streamer_name}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()

                if data.get('data'):
                    if not self.is_live:
                        self.is_live = True
                        channel = self.bot.get_channel(1275830924776574999)
                        await channel.send(f"@everyone , drykai est en stream juste ici --> https://twitch.tv/{self.streamer_name} !")
                        print(f" Alerte stream envoyée pour {self.streamer_name}")
                    else:
                        self.is_live = False

    @check_twitch.before_loop
    async def before_check_twitch(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Twitch(bot))