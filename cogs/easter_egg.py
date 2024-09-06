import discord
from discord.ext import commands
import json
from core.classes import Cog_Extension

with open("setting.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)


class Easter_Egg(Cog_Extension):

    @commands.command()
    async def 陪我玩(self, ctx):

        options = [
            discord.SelectOption(label="九萬畝", value="0"),
            discord.SelectOption(label="傳說對決", value="1"),
            discord.SelectOption(label="不想玩了", value="2"),
        ]
        select = discord.ui.Select(placeholder="泥想玩什麼0.0?", options=options)

        async def on_select_option(interaction: discord.Interaction):
            await interaction.message.delete()
            if select.values[0] == "2":
                playReply = "騙子"
            else:
                playReply = "不要0.0"
            await interaction.response.send_message(f"{playReply}")

        select.callback = on_select_option

        view = discord.ui.View(timeout=15.0)
        view.add_item(select)
        message = await ctx.send(content='', view=view, reference=ctx.message)

        async def on_timeout():
            if not message:
                return
            try:
                await message.delete()
            except discord.NotFound:
                pass

        view.on_timeout = on_timeout

    @commands.command()
    async def 咩保密(self, ctx, message_id):
        if ctx.author.id != 809831210259447870:
            await ctx.send('別調皮啦0.0')
            return
        message = await ctx.channel.fetch_message(message_id)
        await message.delete()


async def setup(bot):
    await bot.add_cog(Easter_Egg(bot))
