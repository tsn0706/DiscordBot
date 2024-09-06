import discord
from discord import app_commands
from datetime import datetime
from core.classes import Cog_Extension
import asyncio

class SilentMembers(Cog_Extension):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='潛水列表', description='列出一整天沒有講話的成員')
    async def silent_members(self, interaction: discord.Interaction):
        await interaction.response.defer()  # 延遲回應

        guild = interaction.guild
        server_name = guild.name  # 取得伺服器名稱
        server_icon = guild.icon.url 
        silent_members = set(guild.members)  # 初始包含所有成員
        silent_members = {member for member in silent_members if not member.bot}  # 排除機器人

        # 獲取當天 0:00 時的時間戳
        today_midnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 建立協程列表，用於並行處理
        tasks = [
            self.check_channel_for_silent_members(channel, silent_members, today_midnight)
            for channel in guild.text_channels
        ]

        # 並行執行所有協程
        await asyncio.gather(*tasks)

        total_silent_count = len(silent_members)
        total_member_count = len([member for member in guild.members if not member.bot]) 
        if total_silent_count > 0:
            silent_members_list = list(silent_members)
            embed_count = (total_silent_count + 23) // 24  # 計算需要多少個嵌入，每個嵌入顯示24個成員

            for i in range(embed_count):
                embed = discord.Embed(
                    title=f"{server_name} 今日的潛水成員列表",
                    description=f"伺服器人數：{total_member_count}\n潛水人數：{total_silent_count}",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=server_icon) 
                
                start_index = i * 24
                end_index = min(start_index + 24, total_silent_count)

                # 每24個成員顯示在一個嵌入中
                for j in range(start_index, end_index):
                    member = silent_members_list[j]
                    display_name = member.display_name
                    # 限制顯示的名字為最多5個中文字，超過部分顯示為省略號
                    if len(display_name) > 5:
                        display_name = display_name[:5] + '...'
                    embed.add_field(name=f"{j + 1}. {display_name}",
                                    value="\u200b",  # 空值，僅為顯示
                                    inline=True)

                embed.set_footer(text="資料統計時間可能會有延遲")
                await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{server_name} 今日的潛水成員列表",
                description=f"伺服器人數：{total_member_count}\n潛水人數：{total_silent_count}\n今日全員換氣！",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=server_icon) 
            await interaction.followup.send(embed=embed)

    async def check_channel_for_silent_members(self, channel, silent_members, today_midnight):
        try:
            async for message in channel.history(after=today_midnight, limit=1000):  # 使用較大的 limit 加速查詢
                if message.author in silent_members:
                    silent_members.remove(message.author)
        except discord.Forbidden:
            pass  # 無法訪問的頻道跳過

async def setup(bot):
    await bot.add_cog(SilentMembers(bot))
