import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension

with open("setting.json","r",encoding="utf8")as jfile:
    jdata = json.load(jfile)

class SoldierConverter(commands.Converter):
    async def convert(self, ctx, argument):
        return argument
    
class SoldierGuide(Cog_Extension):

    @commands.command(name="兵種")
    async def soldier(self, ctx, *, soldier: SoldierConverter):
        if soldier in jdata.get("Soldier", []):
            index = jdata["Soldier"].index(soldier)
            soldierPic = jdata["pic_soldier"][index]
            pic = discord.File(soldierPic)  
            message="本圖由驅邪提供"
            await ctx.send(content=message,file=pic)

    # 註冊一個別名為兵種名稱的指令，方便直接使用 !0.0兵種名稱
    for soldier_name in jdata.get("Soldier", []):
        @commands.command(name=soldier_name.lower())
        async def _soldier(self, ctx, soldier_name=soldier_name):
            await self.soldier(ctx, soldier=soldier_name)

async def setup(bot):
    await bot.add_cog(SoldierGuide(bot))