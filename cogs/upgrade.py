import discord
from discord.ext import commands
from discord import app_commands
import json
from core.classes import Cog_Extension

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

class Upgrade(Cog_Extension):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="建築", description="查看建築資訊")
    @app_commands.describe(建築="選擇一個建築")
    @app_commands.choices(建築=[
        app_commands.Choice(name=building['Type'], value=index)
        for index, building in enumerate(jdata.get("Building", []))
    ])
    async def 建築(self, interaction: discord.Interaction, 建築: int):
        BuildingData = jdata['Building'][建築]
        embed = discord.Embed(title=f"建築資訊-{BuildingData['Type']}")
        BuildPic = BuildingData['pic']
        embed.set_image(url=BuildPic)
        embed.set_footer(text="資料提供：小惟惟\n程式撰寫：14/la & 咩咩")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Upgrade(bot))
