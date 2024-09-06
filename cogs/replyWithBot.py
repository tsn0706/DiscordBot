import discord
from discord.ext import commands

class replWithBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def 發送訊息(self, ctx, channel_id: int = None, message_id: int = None, *, reply_text: str):
        try:
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(message_id)

            # 回覆目標訊息
            await message.reply(reply_text)
            await ctx.message.delete()

        except discord.NotFound:
            await ctx.send("找不到指定的訊息或頻道。")
        except discord.HTTPException as e:
            await ctx.send(f"回覆訊息時發生錯誤：{e}")
        except Exception as e:
            await ctx.send(f"發生未知錯誤：{e}")
    
    @commands.command()
    async def 發送(self, ctx, channel_id: int = None,* , reply_text: str):
        try:
            # 如果提供了 channel_id
            if channel_id:
                channel = self.bot.get_channel(channel_id)
                if not channel:
                    await ctx.send("找不到指定的頻道。")
                    return
                
                # 如果沒有提供 message_id，只發送新訊息到指定頻道
                await channel.send(reply_text)
                await ctx.message.delete()
                return

        except discord.NotFound:
            await ctx.send("找不到指定的訊息或頻道。")
        except discord.HTTPException as e:
            await ctx.send(f"回覆訊息時發生錯誤：{e}")
        except Exception as e:
            await ctx.send(f"發生未知錯誤：{e}")


async def setup(bot):
    await bot.add_cog(replWithBot(bot))
