import discord
import json
from discord import app_commands
from core.classes import Cog_Extension


with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

class SoldierGuide(Cog_Extension):

    def __init__(self, bot):
        self.bot = bot

    async def soldier_choices(self):
        # 從json獲取所有兵種名稱，並返回為 app_commands.Choice 列表
        return [
            app_commands.Choice(name=soldier, value=soldier)
            for soldier in jdata.get("Soldier", [])
        ]
    @app_commands.command(name="兵種", description="查看兵種資訊")
    @app_commands.describe(兵種="選擇一個兵種")
    @app_commands.choices(兵種=[app_commands.Choice(name=soldier, value=soldier) for soldier in jdata.get("Soldier", [])])
    async def soldier(self, interaction: discord.Interaction, 兵種: str):
        soldier = 兵種
        if soldier in jdata.get("Soldier", []):
            index = jdata["Soldier"].index(soldier)
            soldierPic = jdata["pic_soldier"][index]
            embed = discord.Embed()
            embed.add_field(name=f"{soldier}", value="", inline=False)
            embed.set_image(url=soldierPic)
            embed.set_footer(text="圖片提供：驅邪(無更新版本僅供參考)\n程式撰寫：咩咩")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("兵種名稱無效", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SoldierGuide(bot))
