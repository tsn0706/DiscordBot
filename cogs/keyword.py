import discord
import json
import random
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput, View, Button
from core.classes import Cog_Extension

def load_keywords():
    try:
        with open("keyword.json", "r", encoding="utf8") as jfile:
            return json.load(jfile)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# 寫入關鍵字設定
def save_keywords(data):
    try:
        with open("keyword.json", "w", encoding="utf8") as jfile:
            json.dump(data, jfile, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving keywords: {e}")

class KeywordModal(Modal, title="設定關鍵字"):
    InputKeyword = TextInput(
        label="輸入關鍵字", 
        style=discord.TextStyle.long, 
        required=True
    )
    ReplyKeyword = TextInput(
        label="輸入回覆字，在中間加入</咩>會擇一回覆如例",
        style=discord.TextStyle.long,
        placeholder="上巴\n</咩>\n下巴",
        required=True
    )
    ReplyType = TextInput(
        label="回覆類型(相同/包含)", 
        style=discord.TextStyle.short, 
        default="相同",
        max_length=2,
        min_length=2, 
        required=True
    )
    SentType = TextInput(
        label="發送類型(回覆/訊息)", 
        style=discord.TextStyle.short, 
        default="回覆",
        max_length=2,
        min_length=2, 
        required=True
    )
    Hidden = TextInput(
        label="隱藏於列表(是/否)", 
        style=discord.TextStyle.short,
        default="否",
        max_length=1,
        min_length=1, 
        required=True
    )

    def __init__(self, bot, interaction):
        super().__init__()
        self.bot = bot
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        # 取得伺服器ID並儲存禁用關鍵字
        guild_id = str(interaction.guild.id)
        keyword_data = {
            'keyword': self.InputKeyword.value,
            'reply': self.ReplyKeyword.value.split('</咩>'),
            'reply_type': self.ReplyType.value,
            'sent_type': self.SentType.value,
            'hidden': self.Hidden.value
        }
        valid_reply_types = ["相同", "包含"]  # 假設的有效回覆類型
        valid_sent_types = ["回覆", "訊息"]  # 假設的有效發送類型
        valid_hidden_values = ["是", "否"]  # 假設的有效隱藏選項

        # 檢查輸入值是否正確
        if keyword_data['reply_type'] not in valid_reply_types:
            await interaction.response.send_message(f"回覆類型只能是：`{', '.join(valid_reply_types)}`\n你輸入的是：`{keyword_data['reply_type']}`", ephemeral=True)
            return

        if keyword_data['sent_type'] not in valid_sent_types:
            await interaction.response.send_message(f"發送類型只能是：`{', '.join(valid_sent_types)}`\n你輸入的是：`{keyword_data['sent_type']}`", ephemeral=True)
            return

        if keyword_data['hidden'] not in valid_hidden_values:
            await interaction.response.send_message(f"隱藏只能是：`{', '.join(valid_hidden_values)}`\n你輸入的是：`{keyword_data['hidden']}`", ephemeral=True)
            return

        # 獲取關鍵字模組並檢查是否存在此關鍵字
        keyword_cog = self.bot.get_cog('KeywordReply')
        if guild_id not in keyword_cog.keyword_dict:
            keyword_cog.keyword_dict[guild_id] = []

        keyword_exists = False
        for kw in keyword_cog.keyword_dict[guild_id]:
            if kw['keyword'] == self.InputKeyword.value:
                kw.update(keyword_data)
                keyword_exists = True
                break

        if not keyword_exists:
            keyword_cog.keyword_dict[guild_id].append(keyword_data)
        save_keywords(keyword_cog.keyword_dict)  # 保存更新後的數據到 JSON
        guild = interaction.guild
        embed = discord.Embed(title=f"已新增關鍵字", color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="關鍵字", value=f"`{self.InputKeyword.value}`", inline=False)
        embed.add_field(name="回覆詞", value=f"`{self.ReplyKeyword.value}`", inline=False)
        embed.add_field(name="回覆類型", value=f"`{self.ReplyType.value}`", inline=False)
        embed.add_field(name="發送類型", value=f"`{self.SentType.value}`", inline=False)
        embed.add_field(name="隱藏", value=f"`{self.Hidden.value}`", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class KeywordReply(Cog_Extension):

    def __init__(self, bot):
        self.bot = bot
        self.keyword_dict = load_keywords()  # 存儲伺服器對應的關鍵字

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # 忽略機器人訊息
        
        guild_id = str(message.guild.id)
        if guild_id in self.keyword_dict:
            for keyword_data in self.keyword_dict[guild_id]:
                keyword = keyword_data['keyword']
                reply = keyword_data['reply']
                if (keyword_data['reply_type'] == "相同" and keyword == message.content) or \
                   (keyword_data['reply_type'] == '包含' and keyword in message.content):
                    response = reply[0] if len(reply) == 1 else random.choice(reply)
                    if keyword_data['sent_type'] == "回覆":
                        await message.reply(response)
                    else:
                        await message.channel.send(response)

    async def keyword_autocomplete(self, interaction: discord.Interaction, current: str):
        guild_id = str(interaction.guild.id)
        choices = []
        if guild_id in self.keyword_dict:
            # 根據用戶的輸入來過濾關鍵字
            for keyword_data in self.keyword_dict[guild_id]:
                if keyword_data['hidden'] == "否":
                    if current.lower() in keyword_data['keyword'].lower():
                        choices.append(app_commands.Choice(name=keyword_data['keyword'], value=keyword_data['keyword']))
        return choices

    @app_commands.command(name='添加關鍵字', description='添加想觸發的關鍵字')
    async def set_keyword(self, interaction: discord.Interaction):
        # 彈出表單讓用戶輸入關鍵字
        modal = KeywordModal(self.bot, interaction)
        await interaction.response.send_modal(modal)

    @app_commands.command(name='移除關鍵字', description='移除選擇的關鍵字')
    @app_commands.autocomplete(移除=keyword_autocomplete)
    async def remove_keyword(self, interaction: discord.Interaction, 移除: str):
        guild_id = str(interaction.guild.id)
        if guild_id in self.keyword_dict:
            before_count = len(self.keyword_dict[guild_id])
            self.keyword_dict[guild_id] = [kw for kw in self.keyword_dict[guild_id] if kw['keyword'] != 移除]
            after_count = len(self.keyword_dict[guild_id])

            if before_count == after_count:
                await interaction.response.send_message(f"無關鍵字：`{移除}`。", ephemeral=True)
            else:
                save_keywords(self.keyword_dict)
                await interaction.response.send_message(f"已移除關鍵字：`{移除}`。", ephemeral=True)
        else:
            await interaction.response.send_message("還未設定關鍵字噢", ephemeral=True)
    
    @app_commands.command(name='關鍵字列表', description='查看所有關鍵字設定')
    
    async def list_keywords(self, interaction: discord.Interaction):
        guild = interaction.guild
        guild_id = str(interaction.guild.id)
        if guild_id not in self.keyword_dict or not self.keyword_dict[guild_id]:
            await interaction.response.send_message("還未設定關鍵字噢", ephemeral=True)
            return
        
        items_per_page = 6
        hidden_keywords_count = sum(1 for kw in self.keyword_dict[guild_id] if kw['hidden'] == "是")
        visible_keywords = [kw for kw in self.keyword_dict[guild_id] if kw['hidden'] == "否"]

        if not visible_keywords:
            await interaction.response.send_message("沒有可見的關鍵字", ephemeral=True)
            return

        pages = (len(self.keyword_dict[guild_id]) + items_per_page - 1) // items_per_page
        current_page = 0

        def get_page_embed(page_number):

            start = page_number * items_per_page
            end = min(start + items_per_page, len(visible_keywords))
            keywords = visible_keywords[start:end]
            
            embed = discord.Embed(title=f"{guild.name} 的關鍵字列表-共有{len(visible_keywords)}(+{hidden_keywords_count})個", color=discord.Color.blue())
            embed.set_thumbnail(url=guild.icon.url)

            for keyword_data in keywords:
                keyword = keyword_data['keyword']
                replies = '\n'.join(keyword_data['reply'])
                reply_type = keyword_data['reply_type']
                sent_type = keyword_data['sent_type']
                embed.add_field(
                    name=f"關鍵字：`{keyword}`",
                    value=(
                        f"回覆詞：\n`{replies}`\n"
                        f"`{reply_type}`/`{sent_type}`\n"
                        ),
                    inline=True
                )
            embed.set_footer(text=f"{page_number + 1} / {pages}")
            return embed
        
        class PaginatorView(View):
            def __init__(self):
                super().__init__(timeout=60)
                self.current_page = current_page
                self.update_buttons()

            def update_buttons(self):
                self.previous_page.disabled = (self.current_page == 0)
                self.next_page.disabled = (self.current_page == pages - 1)

            @discord.ui.button(label="上一頁", style=discord.ButtonStyle.primary)
            async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
                if self.current_page > 0:
                    self.current_page -= 1
                    try:
                        await self.update_message(interaction)
                    except Exception as e:
                        print(f"Error on previous page: {e}")

            @discord.ui.button(label="下一頁", style=discord.ButtonStyle.primary)
            async def next_page(self,interaction: discord.Interaction, button: discord.ui.Button):
                if self.current_page < pages - 1:
                    self.current_page += 1
                    try:
                        await self.update_message(interaction)
                    except Exception as e:
                        print(f"Error on next page: {e}")

            async def update_message(self, interaction: discord.Interaction):
                embed = get_page_embed(self.current_page)
                self.update_buttons()
                try:
                    await interaction.response.edit_message(embed=embed, view=self)
                except Exception as e:
                    print(f"Error editing message: {e}")

        view = PaginatorView()
        embed = get_page_embed(0)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(KeywordReply(bot))
