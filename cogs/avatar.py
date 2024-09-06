import discord
import json
import aiohttp
from discord import app_commands
from core.classes import Cog_Extension

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

class Avatar(Cog_Extension):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='頭像', description='查看成員的頭像')
    @app_commands.describe(使用者='選擇要查看頭像的成員')
    async def get_avatar(self, interaction: discord.Interaction, 使用者: discord.Member = None):
        if 使用者 is None:
            # 如果未提供成員，則使用命令的作者
            使用者 = interaction.user

        avatar_url = 使用者.avatar.url if 使用者.avatar else 使用者.default_avatar.url
        await interaction.response.send_message(f"{avatar_url}")
    
    # 幫機器人換頭像

    # @app_commands.command(name='換頭像', description='更新機器人的頭像')
    # @app_commands.describe(url='提供一個圖片 URL 或上傳圖片附件來更新頭像')
    # async def set_avatar(self, interaction: discord.Interaction, url: str = None):
    #     if interaction.message.attachments:  # 檢查是否有圖片附件
    #         attachment = interaction.message.attachments[0]
    #         if attachment.content_type.startswith('image/'):  
    #             image_data = await attachment.read()  
    #             await interaction.bot.user.edit(avatar=image_data)  
    #             await interaction.response.send_message("頭像已更新！")
    #         else:
    #             await interaction.response.send_message("頭像更新失敗")
        
    #     elif url:  # 未提供附件檢查 URL
    #         async with aiohttp.ClientSession() as session:
    #             async with session.get(url) as response:
    #                 if response.status == 200:
    #                     image_data = await response.read()
    #                     await interaction.bot.user.edit(avatar=image_data)
    #                     await interaction.response.send_message("頭像已更新！")
    #                 else:
    #                     await interaction.response.send_message("頭像更新失敗")

async def setup(bot):
    await bot.add_cog(Avatar(bot))
