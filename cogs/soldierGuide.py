import discord
import json
from opencc import OpenCC
from discord.ext import commands
from core.classes import Cog_Extension

with open("setting.json","r",encoding="utf8")as jfile:
    jdata = json.load(jfile)

cc = OpenCC('s2twp')

class SoldierConverter(commands.Converter):
    async def convert(self, ctx, argument):
        return cc.convert(argument.lower())
    
class SoldierGuide(Cog_Extension):

    @commands.command(name="兵種", aliases=["兵种"])
    async def soldier(self, ctx, *, soldier: SoldierConverter):
        if soldier in jdata.get("Soldier", []):
            index = jdata["Soldier"].index(soldier)
            soldierPic = jdata["pic_soldier"][index]
            embed = discord.Embed()
            embed.add_field(name = f"兵種-{soldier}", value = "", inline=False)
            embed.set_image(url = soldierPic)
            embed.set_footer(text="本圖由驅邪提供，無更新版本僅供參考")
            await ctx.send(embed = embed)

    # 註冊一個別名為兵種名稱的指令，方便直接使用 !0.0兵種名稱
    for soldier_name in jdata.get("Soldier", []):
        @commands.command(name=soldier_name.lower())
        async def _soldier(self, ctx, soldier_name=soldier_name):
            await self.soldier(ctx, soldier=soldier_name)

async def setup(bot):
    await bot.add_cog(SoldierGuide(bot))