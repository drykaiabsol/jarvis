import discord
from discord.ext import commands
import asyncio
from config import STUDY_CHANNELS, STUDY_TEXT_CHANNEL
from logger import setup_logger

log = setup_logger("study")

class Study(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configs = {}
        for label, channel_id in STUDY_CHANNELS.items():
            work, pause = label.split("/")
            self.configs[channel_id] = (int(work), int(pause))
        self.study_channel_id = STUDY_TEXT_CHANNEL
        self.active_sessions = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        if after.channel and after.channel.id in self.configs:
            if before.channel is None or before.channel.id != after.channel.id:
                if member.id not in self.active_sessions:
                    work_min, pause_min = self.configs[after.channel.id]
                    log.info(f"Lancement {work_min}/{pause_min} : {member.display_name}")
                    task = asyncio.create_task(self.start_pomodoro(member, work_min, pause_min))
                    self.active_sessions[member.id] = task

        if before.channel and before.channel.id in self.configs:
            if after.channel is None or after.channel.id != before.channel.id:
                if member.id in self.active_sessions:
                    log.info(f"Arrêt session : {member.display_name}")
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