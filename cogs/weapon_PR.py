import discord
import json
import asyncio
from discord import app_commands
from core.classes import Cog_Extension

import sys
sys.path.append("../function/")

import function.weapon as wp

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class WeaponPR(Cog_Extension):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="裝備", description="查看裝備資訊")
    @app_commands.describe(裝備="選擇一件裝備")
    @app_commands.choices(
        裝備=[
            app_commands.Choice(name=equipment, value=index)
            for index, equipment in enumerate(jdata.get("Equipment", []))
        ]
    )
    async def 裝備(self, interaction: discord.Interaction, 裝備: int):
        # 確認選擇的裝備是否有效
        if 裝備 < 0 or 裝備 >= len(jdata.get("Equipment", [])):
            await interaction.response.send_message("無效的裝備選擇。", ephemeral=True)
            return

        EquipmentData = jdata['Equipment'][裝備]

        if 裝備 == 0:
            msg_content = f"{EquipmentData} 輸入裝備數值(不填請輸入0)\n格式：0 0 40 180\n第一數值：士兵攻擊力(可不填)\n第二數值：裝備攻擊力(可不填)\n第三數值：爆擊機率\n第四數值：爆擊效果"
        elif 裝備 == 1:
            msg_content = f"{EquipmentData} 輸入裝備數值(不填請輸入0)\n格式：0 0 50 100\n第一數值：士兵攻擊力(可不填)\n第二數值：裝備攻擊力(可不填)\n第三數值：擴散機率\n第四數值：擴散效果"

        await interaction.response.send_message(msg_content, ephemeral=True)

        # 等待用戶輸入數值
        def check(msg):
            return msg.author == interaction.user and msg.channel == interaction.channel

        try:
            response = await self.bot.wait_for("message", check=check, timeout=120.0)
            input_format = response.content.split()
            if len(input_format) == 4 and all(part.isdigit() for part in input_format):
                soldierDamage, damage, probability, effect = map(int, input_format)

                if 裝備 == 0:
                    EquipmentValue = wp.CritBlade(soldierDamage, damage, probability, effect)
                else:
                    EquipmentValue = wp.QiankunSaber(soldierDamage, damage, probability, effect)

                embed = discord.Embed(title=f"裝備-{EquipmentData}")

                if EquipmentValue.PR is None:
                    embed.add_field(name="你的數值", value=f"{EquipmentValue.soldierDamage} {EquipmentValue.damage} {EquipmentValue.probability} {EquipmentValue.effect}", inline=False)
                    embed.add_field(name="404 Not Found", value="`數值錯誤`", inline=True)
                else:
                    embed.add_field(name="你的數值", value=f"{EquipmentValue.soldierDamage} {EquipmentValue.damage} {EquipmentValue.probability} {EquipmentValue.effect}", inline=False)
                    embed.add_field(name="評價", value=f"`{EquipmentValue.PR}`", inline=True)
                    embed.add_field(name="備註", value=f"`{EquipmentValue.ConvertDamage}`", inline=True)

                embed.set_footer(text="若未輸入士兵攻擊力以1等獵人計算\n程式撰寫：14/la & 咩咩")
                await interaction.channel.send(embed=embed)
            else:
                await interaction.channel.send("格式錯誤，請重新輸入數值。", ephemeral=True)

        except asyncio.TimeoutError:
            await interaction.channel.send("超過時間限制，請重新選擇裝備。", ephemeral=True)

async def setup(bot):
    await bot.add_cog(WeaponPR(bot))
