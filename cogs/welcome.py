import discord
from discord.ext import commands
from config import MEMBER_ROLE_NAME
from logger import setup_logger

log = setup_logger("welcome")

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=MEMBER_ROLE_NAME)
        if not role:
            log.warning(f"Rôle '{MEMBER_ROLE_NAME}' introuvable sur {member.guild.name}")
            return
        await member.add_roles(role)
        log.info(f"Rôle '{MEMBER_ROLE_NAME}' attribué à {member.display_name}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
