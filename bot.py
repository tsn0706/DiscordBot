import os
import asyncio
import discord
import json
from discord.ext import commands

#讀取json檔
with open("setting.json","r",encoding="utf8")as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = jdata["CommandPrefix"], intents = intents)

@bot.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', bot.user)
    game = discord.Game('窩ㄞ咩咩')#暱稱欄位文字
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_command_error(ctx, error):#前綴輸入正確但指令錯誤時
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("無指令\n輸入: \" !咩指令 \" 了解更多噢")

# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")

# 卸載指令檔案
@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")

# 重新載入程式檔案
@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")

# 一開始bot開機需載入全部程式檔案
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(filename)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(jdata["TOKEN"])

# 確定執行此py檔才會執行
if __name__ == "__main__":
    asyncio.run(main())
