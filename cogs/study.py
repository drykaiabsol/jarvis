import discord
from discord.ext import commands
import asyncio

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_voice_channel_id = 1482535753325088889
        self.study_channel_id = 1482758719942168809
        self.active_sessions = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        if after.channel and after.channel.id == self.target_voice_channel_id:
            if before.channel is None or before.channel.id != after.channel.id:
                if member.id not in self.active_sessions:
                    print(f"Lancement Pomodoro : {member.display_name}")
                    task = asyncio.create_task(self.start_pomodoro(member))
                    self.active_sessions[member.id] = task

        if before.channel and before.channel.id == self.target_voice_channel_id:
            if after.channel is None or after.channel.id != self.target_voice_channel_id:
                if member.id in self.active_sessions:
                    print(f"Arrêt Pomodoro : {member.display_name}")
                    self.active_sessions[member.id].cancel()
                    del self.active_sessions[member.id]

    async def start_pomodoro(self, member):
        channel = self.bot.get_channel(self.study_channel_id)
        if not channel: return

        try:
            while True:
                await channel.send(f"⏳ **SESSION DE TRAVAIL** (25 min) pour {member.mention}")
                await asyncio.sleep(25 * 60)
                
                await channel.send(f"☕ **PAUSE** (5 min) pour {member.mention}")
                await asyncio.sleep(5 * 60)
        except asyncio.CancelledError:
            await channel.send(f"🏁 Session terminée pour {member.mention} !")

async def setup(bot):
    await bot.add_cog(Study(bot))