import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension

with open("setting.json","r",encoding="utf8")as jfile:
    jdata = json.load(jfile)
class gretings(Cog_Extension):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = int(jdata["Guild"]) 
        if member.guild.id == guild_id:
            channel = self.bot.get_channel(int(jdata["Member_channel"]))
            await channel.send(f"{member.mention}歡迎參觀咩咩教堂")
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        guild_id = int(jdata["Guild"]) 
        if member.guild.id == guild_id:
            channel = self.bot.get_channel(int(jdata["Member_channel"]))
            await channel.send(f"{member.mention}離開咩咩身邊惹")

async def setup(bot):
    await bot.add_cog(gretings(bot))
