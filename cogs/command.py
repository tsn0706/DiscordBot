import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Command(Cog_Extension):

    @commands.command(name="指令")
    async def soldier(self, ctx):
        embed = discord.Embed()
        embed.add_field(
            name="命令咩咩的種類",
            value="/咩裝備\n/咩兵種 xx\n/咩建築\n/咩頭像 @xxx\n/咩換頭像 [圖片連結]",
            inline=False
        )
        embed.set_footer(text="機器人製作：14(la) & 咩咩")
        await ctx.send(embed=embed, reference=ctx.message)


async def setup(bot):
    await bot.add_cog(Command(bot))
