import discord
from discord.ext import commands
import asyncio

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configs = {
            1482535753325088889: (25, 5),
            1482535885043142688: (50, 10),
            1483499790699462778: (90, 20)
        }
        self.study_channel_id = 1482758719942168809
        self.active_sessions = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        if after.channel and after.channel.id in self.configs:
            if before.channel is None or before.channel.id != after.channel.id:
                if member.id not in self.active_sessions:
                    work_min, pause_min = self.configs[after.channel.id]
                    print(f"Lancement {work_min}/{pause_min} : {member.display_name}")
                    task = asyncio.create_task(self.start_pomodoro(member, work_min, pause_min))
                    self.active_sessions[member.id] = task

        if before.channel and before.channel.id in self.configs:
            if after.channel is None or after.channel.id != before.channel.id:
                if member.id in self.active_sessions:
                    print(f"Arrêt session : {member.display_name}")
                    self.active_sessions[member.id].cancel()
                    del self.active_sessions[member.id]

    async def start_pomodoro(self, member, work_min, pause_min):
        channel = self.bot.get_channel(self.study_channel_id)
        if not channel: return

        try:
            while True:
                await channel.send(f"⏳ **SESSION DE TRAVAIL** ({work_min} min) pour {member.mention}")
                await asyncio.sleep(work_min * 60)
                
                await channel.send(f"☕ **PAUSE** ({pause_min} min) pour {member.mention}")
                await asyncio.sleep(pause_min * 60)
        except asyncio.CancelledError:
            await channel.send(f"🏁 Session terminée pour {member.mention} !")

async def setup(bot):
    await bot.add_cog(Study(bot))